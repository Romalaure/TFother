"""Checks that every icon used by the generated books exists in the given jars.

Usage: python tools/books/check_icons.py <minecraft-resources.jar> <tensura.jar> <minecolonies.jar>
"""
import glob
import json
import os
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BOOKS = os.path.join(ROOT, "src", "main", "resources", "assets", "tfother", "patchouli_books")

known = set()
for jar in sys.argv[1:]:
    with zipfile.ZipFile(jar) as z:
        for n in z.namelist():
            parts = n.split("/")
            if len(parts) == 5 and parts[0] == "assets" and parts[2:4] == ["models", "item"] and n.endswith(".json"):
                known.add(parts[1] + ":" + parts[4][:-5])

missing = set()
for f in glob.glob(os.path.join(BOOKS, "**", "*.json"), recursive=True):
    with open(f, encoding="utf-8") as fh:
        data = json.load(fh)
    if data["icon"] not in known:
        missing.add(data["icon"])
    if "category" in data:
        book = os.path.relpath(f, BOOKS).split(os.sep)[0]
        cat = data["category"].split(":")[1]
        if not os.path.exists(os.path.join(BOOKS, book, "en_us", "categories", cat + ".json")):
            print("Unknown category", data["category"], "in", f)

print("Missing icons:", sorted(missing) if missing else "none")
