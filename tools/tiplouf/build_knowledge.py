# -*- coding: utf-8 -*-
"""Builds Tiplouf's knowledge base from the Tensura mods of the Timefield modpack.

Usage: python tools/tiplouf/build_knowledge.py [mods.json URL]

1. Reads the modpack mod list and finds, with HTTP range requests (only each jar's
   mods.toml is downloaded), the mods that depend on Tensura.
2. Downloads those jars into tools/tiplouf/.cache/.
3. Extracts wiki books (Patchouli), skill/race/enchantment descriptions, items and how
   to obtain them (mob drops, chests, ores, special stations), mobs and where they spawn,
   and structures.
4. Writes src/main/resources/data/tfother/tiplouf/knowledge.json, a list of text chunks
   searched at runtime by the NPC.
"""

import json
import os
import re
import struct
import sys
import urllib.parse
import urllib.request
import zipfile
import zlib
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, "tools", "tiplouf", ".cache")
OUT = os.path.join(ROOT, "src", "main", "resources", "data", "tfother", "tiplouf", "knowledge.json")
TFOTHER_BOOK = os.path.join(ROOT, "src", "main", "resources", "assets", "tfother", "patchouli_books", "tensura", "en_us")
DEFAULT_MODS_URL = "https://timefield.tidic.fr/res/mods.json"

# Crafting types players already see in JEI: we only say "craftable" for these.
PLAIN_CRAFTING = {"minecraft:crafting_shaped", "minecraft:crafting_shapeless", "minecraft:smelting",
                  "minecraft:blasting", "minecraft:smoking", "minecraft:campfire_cooking",
                  "minecraft:stonecutting", "minecraft:smithing_transform", "minecraft:smithing_trim"}
MAX_CHUNK_CHARS = 1500
MAX_LIST = 12


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def http_get(url, byte_range=None):
    req = urllib.request.Request(url, headers={"User-Agent": "TFother-knowledge-builder"})
    if byte_range:
        req.add_header("Range", "bytes=%d-%d" % byte_range)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def remote_mods_toml(url, size):
    """Reads META-INF/(neoforge.)mods.toml from a remote jar using range requests."""
    tail_len = min(size, 65536 + 22)
    tail = http_get(url, (size - tail_len, size - 1))
    eocd = tail.rfind(b"PK\x05\x06")
    if eocd < 0:
        return ""
    cd_size, cd_offset = struct.unpack("<II", tail[eocd + 12:eocd + 20])
    tail_start = size - tail_len
    if cd_offset >= tail_start:
        cd = tail[cd_offset - tail_start:cd_offset - tail_start + cd_size]
    else:
        cd = http_get(url, (cd_offset, cd_offset + cd_size - 1))
    pos = 0
    while pos + 46 <= len(cd) and cd[pos:pos + 4] == b"PK\x01\x02":
        method, = struct.unpack("<H", cd[pos + 10:pos + 12])
        comp_size, = struct.unpack("<I", cd[pos + 20:pos + 24])
        name_len, extra_len, comment_len = struct.unpack("<HHH", cd[pos + 28:pos + 34])
        local_offset, = struct.unpack("<I", cd[pos + 42:pos + 46])
        name = cd[pos + 46:pos + 46 + name_len].decode("utf-8", "replace")
        pos += 46 + name_len + extra_len + comment_len
        if name in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
            header = http_get(url, (local_offset, local_offset + 29))
            n_len, e_len = struct.unpack("<HH", header[26:30])
            start = local_offset + 30 + n_len + e_len
            data = http_get(url, (start, start + comp_size - 1))
            if method == 8:
                data = zlib.decompress(data, -15)
            return data.decode("utf-8", "replace")
    return ""


def local_mods_toml(path):
    with zipfile.ZipFile(path) as z:
        for name in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
            if name in z.namelist():
                return z.read(name).decode("utf-8", "replace")
    return ""


def is_tensura_mod(toml):
    """Tensura, its addons and mods that mention it (e.g. the Patchouli Tensura wiki).

    TFother is skipped: its own Tensura book is read from the sources.
    """
    lower = toml.lower()
    return "tensura" in lower and 'modid="tfother"' not in lower.replace(" ", "")


def fetch_tensura_jars(mods_url):
    mods = json.loads(http_get(mods_url))["mods"]
    os.makedirs(CACHE, exist_ok=True)

    def check(mod):
        name = urllib.parse.unquote(mod["name"])
        path = os.path.join(CACHE, name)
        cached = os.path.exists(path) and os.path.getsize(path) == mod["size"]
        try:
            toml = local_mods_toml(path) if cached else remote_mods_toml(mod["downloadURL"], mod["size"])
            if not is_tensura_mod(toml):
                return None
            if cached:
                return path
        except Exception as e:  # noqa: BLE001 - one bad jar must not stop the build
            print("  ! %s: %s" % (name, e))
            return None
        with open(path, "wb") as f:
            f.write(http_get(mod["downloadURL"]))
        return path

    with ThreadPoolExecutor(8) as pool:
        return sorted(p for p in pool.map(check, mods) if p)


# ---------------------------------------------------------------------------
# Jar reading
# ---------------------------------------------------------------------------

class Data:
    def __init__(self):
        self.en = {}
        self.fr = {}
        self.mod_ids = set()
        self.mod_names = {}
        self.namespaces = set()
        self.books = []            # (mod, entry dict, lang dict)
        self.loot = {}             # table id -> json
        self.recipes = []          # (id, json)
        self.spawns = []           # (entity, biomes)
        self.biome_tags = {}       # tag id -> values
        self.structures = {}       # structure id -> json


def read_json(z, name):
    try:
        return json.loads(z.read(name).decode("utf-8-sig"))
    except Exception:  # noqa: BLE001 - some mods ship json5/comments, skip them
        return None


def resource_id(path, folder):
    """data/<ns>/<folder>/<path>.json -> ns:path"""
    parts = path.split("/")
    ns = parts[1]
    rest = "/".join(parts[3 + folder.count("/"):])
    return ns + ":" + rest[:-5]


def load_jar(path, data):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    toml = next((n for n in names if n in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml")), None)
    if toml:
        text = z.read(toml).decode("utf-8", "replace")
        mod_ids = re.findall(r'\[\[mods\]\][^\[]*?modId\s*=\s*"([^"]+)"', text, re.S)
        disp = re.findall(r'displayName\s*=\s*"([^"]+)"', text)
        for i, mid in enumerate(mod_ids):
            data.mod_ids.add(mid)
            data.mod_names[mid] = disp[i] if i < len(disp) else mid
    for n in names:
        if not n.endswith(".json"):
            continue
        m = re.match(r"assets/([^/]+)/lang/(en_us|fr_fr)\.json$", n)
        if m:
            data.namespaces.add(m.group(1))
            lang = read_json(z, n) or {}
            (data.en if m.group(2) == "en_us" else data.fr).update(lang)
            continue
        m = re.match(r"assets/([^/]+)/patchouli_books/([^/]+)/en_us/entries/(.+)\.json$", n)
        if m:
            entry = read_json(z, n)
            if entry:
                data.books.append((m.group(1), entry))
            continue
        if not n.startswith("data/"):
            continue
        parts = n.split("/")
        if len(parts) < 4:
            continue
        data.namespaces.add(parts[1])
        kind = parts[2]
        if kind in ("loot_table", "loot_tables"):
            j = read_json(z, n)
            if j:
                data.loot[resource_id(n, kind)] = j
        elif kind == "recipe" or kind == "recipes":
            j = read_json(z, n)
            if isinstance(j, dict):
                data.recipes.append((resource_id(n, kind), j))
        elif kind == "neoforge" and parts[3] == "biome_modifier":
            j = read_json(z, n)
            if isinstance(j, dict) and j.get("type") == "neoforge:add_spawns":
                spawners = j.get("spawners")
                spawners = spawners if isinstance(spawners, list) else [spawners]
                for s in spawners:
                    if isinstance(s, dict) and "type" in s:
                        data.spawns.append((s["type"], j.get("biomes")))
        elif kind == "tags" and "/".join(parts[3:5]) == "worldgen/biome":
            j = read_json(z, n)
            if j:
                data.biome_tags[resource_id(n, "tags/worldgen/biome")] = j.get("values", [])
        elif kind == "worldgen" and parts[3] == "structure":
            j = read_json(z, n)
            if j:
                data.structures[resource_id(n, "worldgen/structure")] = j


# ---------------------------------------------------------------------------
# Naming helpers
# ---------------------------------------------------------------------------

def pretty(rid):
    return rid.split(":")[-1].split("/")[-1].replace("_", " ").strip().capitalize()


def names_for(data, rid, kinds=("item", "block", "entity")):
    if ":" not in rid:
        return pretty(rid), None
    ns, path = rid.split(":", 1)
    for kind in kinds:
        key = "%s.%s.%s" % (kind, ns, path.replace("/", "."))
        if key in data.en:
            return data.en[key], data.fr.get(key)
    return pretty(rid), None


def label(data, rid, kinds=("item", "block", "entity")):
    en, fr = names_for(data, rid, kinds)
    return "%s / %s" % (en, fr) if fr and fr != en else en


def strip_codes(text):
    return re.sub(r"\u00a7.?", "", text)


def clean_patchouli(text, data):
    if not isinstance(text, str):
        return ""
    if text in data.en:
        text = data.en[text]
    text = strip_codes(text)
    text = text.replace("$(br2)", "\n").replace("$(br)", "\n").replace("$(li)", "\n- ").replace("$(br)", "\n")
    text = re.sub(r"\$\(l:[^)]*\)", "", text)
    text = re.sub(r"\$\([^)]*\)", "", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def flag_ok(flag, data):
    if not flag:
        return True
    for part in re.split(r"[,|]", flag.strip("&|")):
        part = part.strip()
        neg = part.startswith("!")
        part = part.lstrip("!")
        if part.startswith("mod:"):
            present = part[4:] in data.mod_ids or part[4:] in ("minecraft", "neoforge")
            if present == neg:
                return False
    return True


def short_list(items):
    items = sorted(set(items))
    if len(items) > MAX_LIST:
        return ", ".join(items[:MAX_LIST]) + " (+%d autres)" % (len(items) - MAX_LIST)
    return ", ".join(items)


# ---------------------------------------------------------------------------
# Loot and recipes
# ---------------------------------------------------------------------------

def loot_items(node, out):
    """Collects every item name referenced by a loot table (nested entries included)."""
    if isinstance(node, dict):
        if node.get("type") in ("minecraft:item", "item") and isinstance(node.get("name"), str):
            out.add(node["name"])
        for v in node.values():
            loot_items(v, out)
    elif isinstance(node, list):
        for v in node:
            loot_items(v, out)
    return out


def recipe_output(recipe):
    for key in ("result", "output", "results", "outputs"):
        if key in recipe:
            val = recipe[key]
            while True:
                val = val[0] if isinstance(val, list) and val else val
                if isinstance(val, str):
                    return val
                if not isinstance(val, dict):
                    return None
                val = val.get("id") or val.get("item")


def recipe_inputs(recipe):
    out = []

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("tag"), str):
                out.append("#" + node["tag"])
                return
            for k in ("item", "id"):
                if isinstance(node.get(k), str):
                    out.append(node[k])
                    return
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk({k: v for k, v in recipe.items() if k not in ("result", "output", "results", "outputs")})
    return out


# ---------------------------------------------------------------------------
# Chunks
# ---------------------------------------------------------------------------

def add_chunk(chunks, title, text, source):
    text = text.strip()
    if not text:
        return
    while len(text) > MAX_CHUNK_CHARS:
        cut = text.rfind("\n", 0, MAX_CHUNK_CHARS)
        cut = cut if cut > MAX_CHUNK_CHARS // 2 else MAX_CHUNK_CHARS
        chunks.append({"title": strip_codes(title), "text": strip_codes(text[:cut].strip()), "source": source})
        text = text[cut:].strip()
        title = title if title.endswith("(suite)") else title + " (suite)"
    chunks.append({"title": strip_codes(title), "text": strip_codes(text), "source": source})


def book_chunks(data, chunks):
    for mod, entry in data.books:
        if not flag_ok(entry.get("flag"), data):
            continue
        title = clean_patchouli(entry.get("name", ""), data)
        parts = []
        for page in entry.get("pages", []):
            if not isinstance(page, dict):
                continue
            if page.get("title"):
                parts.append(clean_patchouli(page["title"], data))
            if isinstance(page.get("item"), str):
                parts.append("[" + label(data, page["item"].split("{")[0].split(",")[0]) + "]")
            if page.get("text"):
                parts.append(clean_patchouli(page["text"], data))
        add_chunk(chunks, title, "\n".join(p for p in parts if p), "Wiki " + data.mod_names.get(mod, mod))


def tfother_book_chunks(data, chunks):
    entries = os.path.join(TFOTHER_BOOK, "entries")
    for dirpath, _, files in os.walk(entries):
        for f in sorted(files):
            with open(os.path.join(dirpath, f), encoding="utf-8") as fh:
                entry = json.load(fh)
            text = "\n".join(clean_patchouli(p.get("text", ""), data) for p in entry.get("pages", []) if isinstance(p, dict))
            add_chunk(chunks, clean_patchouli(entry.get("name", ""), data), text, "Wiki Tensura Timefield")


def description_chunks(data, chunks):
    kinds = {"skill": "Compétence", "race": "Race", "magic": "Magie", "enchantment": "Enchantement",
             "effect": "Effet", "battlewill": "Battlewill", "attribute": "Attribut"}
    for key, desc in data.en.items():
        m = re.match(r"^(?:(tensura[\w]*|[\w]+)\.)?(skill|race|magic|enchantment|effect|battlewill)\.([\w.]+?)\.(description|desc)$", key)
        if not m:
            continue
        base = key[: -len(m.group(4)) - 1]
        ns = key.split(".")[1] if m.group(2) in ("enchantment", "effect") else key.split(".")[0]
        if ns not in data.namespaces and ns not in data.mod_ids:
            continue
        en = data.en.get(base, pretty(m.group(3)))
        fr = data.fr.get(base)
        name = "%s / %s" % (en, fr) if fr and fr != en else en
        text = desc
        if data.fr.get(key) and data.fr[key] != desc:
            text += "\n(FR) " + data.fr[key]
        add_chunk(chunks, "%s : %s" % (kinds[m.group(2)], name), text, data.mod_names.get(ns, ns))


def item_and_mob_chunks(data, chunks):
    family = data.namespaces
    dropped_by = defaultdict(set)
    chests = defaultdict(set)
    mined = defaultdict(set)
    other_loot = defaultdict(set)
    mob_drops = defaultdict(set)
    chest_contents = defaultdict(set)

    for table, j in data.loot.items():
        ns, path = table.split(":", 1)
        items = loot_items(j, set())
        if path.startswith("entities/"):
            mob = ns + ":" + path[len("entities/"):]
            for it in items:
                dropped_by[it].add(label(data, mob, ("entity",)))
                mob_drops[mob].add(label(data, it))
        elif path.startswith("chests/"):
            for it in items:
                chests[it].add(pretty(path))
                chest_contents[pretty(path)].add(label(data, it))
        elif path.startswith("blocks/"):
            block = ns + ":" + path[len("blocks/"):]
            for it in items:
                if it != block:
                    mined[it].add(label(data, block, ("block",)))
        else:
            for it in items:
                other_loot[it].add(pretty(path))

    stations = defaultdict(set)
    special = defaultdict(list)
    for rid, r in data.recipes:
        out = recipe_output(r)
        rtype = r.get("type", "")
        if not out or not isinstance(rtype, str):
            continue
        if rtype in PLAIN_CRAFTING:
            stations[out].add("craft classique (voir JEI)")
        else:
            station = pretty(rtype)
            stations[out].add(station)
            if len(special[out]) < 2:
                ins = [label(data, i) if not i.startswith("#") else "tag " + i[1:] for i in recipe_inputs(r)][:6]
                if ins:
                    special[out].append("%s : %s" % (station, ", ".join(ins)))

    spawn_biomes = defaultdict(set)
    for entity, biomes in data.spawns:
        spawn_biomes[entity].update(biome_labels(data, biomes))

    seen = set()
    for key in list(data.en):
        m = re.match(r"^(item|block)\.([\w]+)\.([\w./]+)$", key)
        if not m or m.group(2) not in family:
            continue
        rid = m.group(2) + ":" + m.group(3)
        if rid in seen:
            continue
        seen.add(rid)
        lines = []
        for tkey in (key + ".tooltip", key + ".desc", key + ".description", "tooltip." + rid.replace(":", ".")):
            if tkey in data.en:
                lines.append(data.en[tkey])
        if dropped_by.get(rid):
            lines.append("Butin de : " + short_list(dropped_by[rid]))
        if mined.get(rid):
            lines.append("S'obtient en minant/cassant : " + short_list(mined[rid]))
        if chests.get(rid):
            lines.append("Trouvable dans les coffres : " + short_list(chests[rid]))
        if other_loot.get(rid):
            lines.append("Autres sources : " + short_list(other_loot[rid]))
        if stations.get(rid):
            lines.append("Fabrication : " + short_list(stations[rid]))
            lines.extend("Recette " + s for s in special.get(rid, []))
        if not lines:
            continue
        add_chunk(chunks, "Objet : " + label(data, rid), "\n".join(lines), data.mod_names.get(m.group(2), m.group(2)))

    for key in list(data.en):
        m = re.match(r"^entity\.([\w]+)\.([\w./]+)$", key)
        if not m or m.group(1) not in family:
            continue
        rid = m.group(1) + ":" + m.group(2)
        lines = []
        if spawn_biomes.get(rid):
            lines.append("Apparaît naturellement dans : " + short_list(spawn_biomes[rid]))
        if mob_drops.get(rid):
            lines.append("Butin : " + short_list(mob_drops[rid]))
        if not lines:
            continue
        add_chunk(chunks, "Créature : " + label(data, rid, ("entity",)), "\n".join(lines), data.mod_names.get(m.group(1), m.group(1)))

    for sid, j in data.structures.items():
        if sid.split(":")[0] not in family:
            continue
        biomes = biome_labels(data, j.get("biomes"))
        name = pretty(sid.split("/")[0] if "/" in sid.split(":")[1] else sid)
        lines = []
        if biomes:
            lines.append("Génération dans : " + short_list(biomes))
        loot = set()
        for chest, items in chest_contents.items():
            if name.lower().split()[0] in chest.lower():
                loot.update(items)
        if loot:
            lines.append("Coffres : " + short_list(loot))
        if lines:
            add_chunk(chunks, "Structure : " + pretty(sid.replace("/", " ")), "\n".join(lines), data.mod_names.get(sid.split(":")[0], sid))


def biome_labels(data, biomes, depth=0):
    if biomes is None:
        return set()
    if isinstance(biomes, str):
        biomes = [biomes]
    out = set()
    for b in biomes:
        if isinstance(b, dict):
            b = b.get("id", "")
        if not isinstance(b, str):
            continue
        if b.startswith("#"):
            tag = b[1:]
            if tag in data.biome_tags and depth < 3:
                out.update(biome_labels(data, data.biome_tags[tag], depth + 1))
            else:
                out.add("biomes " + pretty(tag))
        else:
            out.add(pretty(b))
    return out


def modlist_chunk(data, chunks):
    names = sorted(set(data.mod_names[m] for m in data.mod_names if m not in ("neoforge", "minecraft")))
    add_chunk(chunks, "Liste des mods Tensura du serveur",
              "Mods liés à Tensura installés sur Timefield : " + ", ".join(names), "Modpack Timefield")


def main():
    mods_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODS_URL
    print("Recherche des mods Tensura dans", mods_url)
    jars = fetch_tensura_jars(mods_url)
    print("%d jars Tensura" % len(jars))
    data = Data()
    for jar in jars:
        load_jar(jar, data)
    data.namespaces &= data.mod_ids | {ns for ns in data.namespaces if ns.startswith("tensura")}

    chunks = []
    modlist_chunk(data, chunks)
    tfother_book_chunks(data, chunks)
    book_chunks(data, chunks)
    description_chunks(data, chunks)
    item_and_mob_chunks(data, chunks)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, separators=(",", ":"))
    print("%d morceaux, %d Ko -> %s" % (len(chunks), os.path.getsize(OUT) // 1024, os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
