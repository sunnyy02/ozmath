#!/usr/bin/env python3
"""Replace paraphrased AC v9.0 text in data/standards.json with official MRAC wording.

Usage:
  1. Download the Mathematics JSON-LD from the Machine-Readable Australian Curriculum
     (https://www.australiancurriculum.edu.au/machine-readable-australian-curriculum)
     into sources/ (for example sources/mrac-mathematics.jsonld).
  2. python3 scripts/ingest_mrac.py sources/mrac-mathematics.jsonld [--dry-run]

What it does: walks every JSON object in the file, and for any object that has a
statement code matching AC9M\\d+... and a description, records code -> text.
Then for each `ac9` item in data/standards.json with the same id it sets
`text` to the official wording, `verbatim: true` and `source` to the MRAC file.
Elaborations (child statements of a content description) are attached as
`elaborations` when they can be identified.

NOTE: written without access to a real MRAC file (the site was unreachable from the
build environment). Key names are matched loosely; run with --dry-run first and
check the counts it prints (Years 9-10 should be 21-23 codes each).
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STD = os.path.join(ROOT, "data", "standards.json")
CODE_RE = re.compile(r"^AC9M(?:\d{1,2}|F)[A-Z]{1,2}\d{2}$")
ELAB_RE = re.compile(r"^(AC9M(?:\d{1,2}|F)[A-Z]{1,2}\d{2})_E\d+$")


def text_of(v):
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        for k in ("@value", "value", "en"):
            if k in v:
                return text_of(v[k])
    if isinstance(v, list):
        for x in v:
            t = text_of(x)
            if t:
                return t
    return None


def pick(obj, keys):
    for k, v in obj.items():
        kl = k.lower()
        if any(kl.endswith(x) for x in keys):
            t = text_of(v)
            if t:
                return t.strip()
    return None


def walk(o, found, elabs):
    if isinstance(o, dict):
        code = pick(o, ("statementnotation", "notation", "code", "humancodingscheme"))
        desc = pick(o, ("description", "text", "preflabel"))
        if code and desc:
            code = code.strip()
            if CODE_RE.match(code):
                found.setdefault(code, desc)
            else:
                m = ELAB_RE.match(code)
                if m:
                    elabs.setdefault(m.group(1), []).append(desc)
        for v in o.values():
            walk(v, found, elabs)
    elif isinstance(o, list):
        for v in o:
            walk(v, found, elabs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mrac")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    with open(a.mrac, encoding="utf-8") as f:
        doc = json.load(f)
    found, elabs = {}, {}
    walk(doc, found, elabs)
    by_year = {}
    for c in found:
        y = re.match(r"AC9M(\d+|F)", c).group(1)
        by_year[y] = by_year.get(y, 0) + 1
    print("codes found by year:", dict(sorted(by_year.items(), key=lambda kv: (kv[0] == "F", kv[0]))))
    with open(STD, encoding="utf-8") as f:
        items = json.load(f)
    hit, miss = 0, []
    for it in items:
        if it.get("framework") != "ac9":
            continue
        if it["id"] in found:
            hit += 1
            it["text"] = found[it["id"]]
            it["verbatim"] = True
            it["source"] = "MRAC v9.0: " + os.path.basename(a.mrac)
            if elabs.get(it["id"]):
                it["elaborations"] = elabs[it["id"]]
        else:
            miss.append(it["id"])
    print("updated %d ac9 items; not found: %s" % (hit, miss or "none"))
    if a.dry_run:
        return
    with open(STD, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", os.path.relpath(STD, ROOT))


if __name__ == "__main__":
    sys.exit(main())
