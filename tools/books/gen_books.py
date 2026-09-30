"""Generates the Patchouli books of TFother from books_content.py.

Run from the repo root:  python tools/books/gen_books.py
Text blocks are paginated automatically so no page overflows.
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from books_content import BOOKS  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "src", "main", "resources")
NS = "tfother"

LINE_PX = 114
FIRST_PAGE_LINES = 12
PAGE_LINES = 15
LI_INDENT = 10

NARROW = {"i": 2, "l": 3, "t": 4, "f": 5, "k": 5, "I": 4, " ": 4, ".": 2, ",": 2, ":": 2,
          ";": 2, "!": 2, "'": 2, "|": 2, "(": 4, ")": 4, "[": 4, "]": 4, "*": 4, '"': 4,
          "î": 4, "ï": 4, "ì": 3, "í": 3, "<": 5, ">": 5, "{": 4, "}": 4, "`": 3, "’": 2}


def char_px(c, bold):
    return NARROW.get(c, 6) + (1 if bold else 0)


def tokenize(text):
    return re.split(r"(\$\([^)]*\))", text)


def count_lines(text):
    """Rough simulation of Patchouli word wrapping; returns the number of lines."""
    lines, x, width, bold = 1, 0, LINE_PX, False
    for tok in tokenize(text):
        if tok.startswith("$("):
            m = tok[2:-1]
            if m == "br":
                lines, x, width = lines + 1, 0, LINE_PX
            elif m == "br2":
                lines, x, width = lines + 2, 0, LINE_PX
            elif m == "li":
                if x > 0:
                    lines += 1
                x, width = 0, LINE_PX - LI_INDENT
            elif m == "l":
                bold = True
            elif m == "":
                bold = False
            continue
        for word in re.split(r"( )", tok):
            if not word:
                continue
            w = sum(char_px(c, bold) for c in word)
            if word == " ":
                x += w
                continue
            if x + w > width and x > 0:
                lines += 1
                x = 0
            x += w
    return lines


def split_block(block, limit):
    """Split a too long block on sentence boundaries."""
    parts = re.split(r"(?<=[.!?:]) ", block)
    out, cur = [], ""
    for p in parts:
        cand = (cur + " " + p).strip()
        if cur and count_lines(cand) > limit:
            out.append(cur)
            cur = p
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out


def paginate(blocks):
    pages, cur = [], ""
    limit = FIRST_PAGE_LINES
    queue = list(blocks)
    while queue:
        b = queue.pop(0)
        if count_lines(b) > limit and not cur:
            pieces = split_block(b, limit)
            if len(pieces) == 1:
                raise SystemExit("Block too long to fit a page: " + b[:80])
            queue = pieces + queue
            continue
        cand = b if not cur else cur + "$(br2)" + b
        if count_lines(cand) <= limit:
            cur = cand
        else:
            pages.append(cur)
            cur, limit = "", PAGE_LINES
            queue.insert(0, b)
    if cur:
        pages.append(cur)
    return pages


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    total_pages = 0
    for book_id, book in BOOKS.items():
        write_json(os.path.join(RES, "data", NS, "patchouli_books", book_id, "book.json"), {
            "name": book["name"],
            "subtitle": book["subtitle"],
            "landing_text": book["landing_text"],
            "model": book["model"],
            "dont_generate_book": True,
            "use_resource_pack": True,
            "show_progress": False,
            "version": 1,
        })
        base = os.path.join(RES, "assets", NS, "patchouli_books", book_id, "en_us")
        shutil.rmtree(base, ignore_errors=True)
        for ci, cat in enumerate(book["categories"]):
            write_json(os.path.join(base, "categories", cat["id"] + ".json"), {
                "name": cat["name"],
                "description": cat["description"],
                "icon": cat["icon"],
                "sortnum": ci,
            })
            for ei, entry in enumerate(cat["entries"]):
                pages = paginate(entry["text"])
                total_pages += len(pages)
                write_json(os.path.join(base, "entries", cat["id"], entry["id"] + ".json"), {
                    "name": entry["name"],
                    "icon": entry["icon"],
                    "category": NS + ":" + cat["id"],
                    "sortnum": ei,
                    "pages": [{"type": "patchouli:text", "text": p} for p in pages],
                })
    print("OK, %d pages generated" % total_pages)


if __name__ == "__main__":
    main()
