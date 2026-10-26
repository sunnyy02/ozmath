#!/usr/bin/env python3
"""Independent blind re-solve of the question bank (the upstream repo's "second pass").

  python3 scripts/blind_pass.py prepare [--size 40]
      Writes data/_blind/blind_NN.json: questions with answer, explanation and verify removed.
      Give each file to a solver (a teacher, or a separate AI session that cannot see data/)
      and ask for data/_blind/ans_NN.json shaped {"<question id>": "<answer>"}.
      Choice answers are a letter; numeric answers use the same format as the prompt asks.

  python3 scripts/blind_pass.py compare
      Compares every ans_NN.json with the bank and writes data/_blind/mismatches.json.
      Each mismatch must be adjudicated by a person: fix the question, or record why the
      solver was wrong in data/blind_pass_log.json.
"""
import argparse
import glob
import json
import os
import re
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLIND = os.path.join(ROOT, "data", "_blind")
KEEP = ("id", "type", "prompt", "choices", "unordered")


def load_questions():
    with open(os.path.join(ROOT, "data", "questions.json"), encoding="utf-8") as f:
        return json.load(f)


def prepare(size):
    os.makedirs(BLIND, exist_ok=True)
    qs = [{k: q[k] for k in KEEP if k in q} for q in load_questions() if q["type"] in ("numeric", "choice", "short")]
    for i in range(0, len(qs), size):
        path = os.path.join(BLIND, "blind_%02d.json" % (i // size + 1))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(qs[i:i + size], f, ensure_ascii=False, indent=1)
    print("wrote %d questions in %d files to %s" % (len(qs), (len(qs) + size - 1) // size, os.path.relpath(BLIND, ROOT)))


def values(s):
    s = s.strip().replace("−", "-")
    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1]
    out = []
    for p in re.split(r",|\band\b|\bor\b", s):
        p = re.sub(r"^\s*[a-z]\s*=\s*", "", p.strip())
        if not p:
            continue
        try:
            out.append(Fraction(p))
        except (ValueError, ZeroDivisionError):
            return None
    return out


def agree(q, given):
    if q["type"] == "choice":
        return given.strip().upper()[:1] == q["answer"]
    a, b = values(q["answer"]), values(str(given))
    if a is None or b is None:
        return q["answer"].replace(" ", "").lower() == str(given).replace(" ", "").lower()
    return sorted(a) == sorted(b) if q.get("unordered") else a == b


def compare():
    bank = {q["id"]: q for q in load_questions()}
    seen, bad = 0, []
    for path in sorted(glob.glob(os.path.join(BLIND, "ans_*.json"))):
        with open(path, encoding="utf-8") as f:
            ans = json.load(f)
        for qid, given in ans.items():
            q = bank.get(qid)
            if not q:
                continue
            seen += 1
            if not agree(q, str(given)):
                bad.append({"id": qid, "keyed": q["answer"], "solver": given, "file": os.path.basename(path)})
    with open(os.path.join(BLIND, "mismatches.json"), "w", encoding="utf-8") as f:
        json.dump(bad, f, ensure_ascii=False, indent=1)
    print("compared %d answers: %d mismatches" % (seen, len(bad)))
    for b in bad:
        print("  %(id)s keyed=%(keyed)s solver=%(solver)s" % b)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prepare", "compare"])
    ap.add_argument("--size", type=int, default=40)
    a = ap.parse_args()
    prepare(a.size) if a.cmd == "prepare" else compare()
