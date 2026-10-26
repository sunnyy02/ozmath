#!/usr/bin/env python3
"""Validate data/*.json (standard library only). Exit code 1 on any error.

Checks
  topics      required fields, id format per band, unique ids, unit on senior topics, level matches band
  edges       known ids, no self-loops/duplicates, acyclic, prerequisite not later than topic,
              track rules (see TRACK below), reason present
  roots       every topic without prerequisites has root_reason
  standards   every topic maps to >= 1 known standard; coverage report of unmapped standards
  questions   >= 4 per topic and >= 2 basic; ids <topic>_qN; choice keys/answers valid; numeric answers parse;
              tech-free topics have >= 2 questions that are not tech: active

Run:  python3 scripts/validate.py [--quiet]
"""
import json
import os
import re
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from qlib import BANDS, SENIOR, level_of, rank_of  # noqa: E402

ID_RE = {
    "y9": re.compile(r"^qm_9_\d{3}$"),
    "y10": re.compile(r"^qm_10_\d{3}$"),
    "y10opt": re.compile(r"^qm_10o_\d{3}$"),
    "general": re.compile(r"^qm_g[1-4]_\d{3}$"),
    "methods": re.compile(r"^qm_m[1-4]_\d{3}$"),
    "specialist": re.compile(r"^qm_s[1-4]_\d{3}$"),
}
TYPES = {"conceptual", "procedural", "reasoning", "application", "modelling"}
TECH = {"free", "active", "either"}
DIFF = {"basic", "standard", "advanced"}
QTYPES = {"numeric", "choice", "short", "self"}
CONF = {"exact", "inferred"}

# band of topic -> bands its prerequisites may come from
TRACK = {
    "y9": {"y9"},
    "y10": {"y9", "y10"},
    "y10opt": {"y9", "y10", "y10opt"},
    "general": {"y9", "y10", "general"},          # General students may not have done the optional content
    "methods": {"y9", "y10", "y10opt", "methods"},
    "specialist": {"y9", "y10", "y10opt", "methods", "specialist"},
}

errors, warnings = [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


def parse_num(s):
    s = s.strip().replace("−", "-")
    try:
        return Fraction(s)
    except (ValueError, ZeroDivisionError):
        return None


def numeric_answer_ok(ans):
    a = ans.strip()
    if a.startswith("(") and a.endswith(")"):
        return all(parse_num(p) is not None for p in a[1:-1].split(","))
    parts = [re.sub(r"^[a-z]\s*=\s*", "", p.strip()) for p in a.split(",")]
    return all(parse_num(p) is not None for p in parts)


def check_topics(topics, std_ids):
    ids = {}
    for t in topics:
        tid = t.get("id", "?")
        for k in ("id", "name", "band", "level", "chapter", "type", "description", "mastery_criteria", "standards", "tech", "status"):
            if k not in t:
                err("%s: missing field %s" % (tid, k))
        if tid in ids:
            err("%s: duplicate id" % tid)
        ids[tid] = t
        band = t.get("band")
        if band not in BANDS:
            err("%s: unknown band %r" % (tid, band))
            continue
        if not ID_RE[band].match(tid):
            err("%s: id does not match band %s" % (tid, band))
        if band in SENIOR:
            if t.get("unit") not in (1, 2, 3, 4):
                err("%s: senior topic needs unit 1-4" % tid)
            elif not tid.startswith("qm_%s%d_" % (band[0], t["unit"])):
                err("%s: id unit does not match unit %s" % (tid, t["unit"]))
        if t.get("level") != level_of(band, t.get("unit")):
            err("%s: level %s does not match band/unit" % (tid, t.get("level")))
        if t.get("type") not in TYPES:
            err("%s: bad type %r" % (tid, t.get("type")))
        if t.get("tech") not in TECH:
            err("%s: bad tech %r" % (tid, t.get("tech")))
        mc = t.get("mastery_criteria") or []
        if not (2 <= len(mc) <= 4):
            err("%s: needs 2-4 mastery criteria" % tid)
        stds = t.get("standards") or []
        if not stds:
            err("%s: maps to no standard" % tid)
        for s in stds:
            if s.get("id") not in std_ids:
                err("%s: unknown standard %s" % (tid, s.get("id")))
            if s.get("confidence") not in CONF:
                err("%s: bad confidence on %s" % (tid, s.get("id")))
    return ids


def find_cycle(ids, prereqs):
    WHITE, GREY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}

    def visit(n, path):
        color[n] = GREY
        for p in prereqs.get(n, []):
            if color[p] == GREY:
                return path + [n, p]
            if color[p] == WHITE:
                c = visit(p, path + [n])
                if c:
                    return c
        color[n] = BLACK
        return None

    for i in ids:
        if color[i] == WHITE:
            c = visit(i, [])
            if c:
                return c
    return None


def check_edges(deps, ids):
    prereqs, seen = {}, set()
    for d in deps:
        a, b = d.get("topicId"), d.get("prerequisiteId")
        if a not in ids or b not in ids:
            err("edge %s -> %s: unknown id" % (a, b))
            continue
        if a == b:
            err("edge %s -> itself" % a)
        if (a, b) in seen:
            err("edge %s -> %s: duplicate" % (a, b))
        seen.add((a, b))
        if d.get("strength") not in ("hard", "soft"):
            err("edge %s -> %s: strength must be hard or soft" % (a, b))
        if not (d.get("reason") or "").strip():
            err("edge %s -> %s: missing reason" % (a, b))
        ta, tb = ids[a], ids[b]
        if rank_of(tb["band"], tb.get("unit")) > rank_of(ta["band"], ta.get("unit")):
            err("edge %s -> %s: prerequisite comes later (%s %s > %s %s)" % (
                a, b, tb["band"], tb.get("unit", ""), ta["band"], ta.get("unit", "")))
        if tb["band"] not in TRACK[ta["band"]]:
            err("edge %s -> %s: track rule, %s topics may not depend on %s" % (a, b, ta["band"], tb["band"]))
        if ta["band"] == "specialist" and tb["band"] == "methods" and tb.get("unit", 0) > ta.get("unit", 0):
            err("edge %s -> %s: Specialist unit %s cannot need a later Methods unit %s" % (a, b, ta["unit"], tb["unit"]))
        prereqs.setdefault(a, []).append(b)
    cyc = find_cycle(ids, prereqs)
    if cyc:
        err("cycle: " + " -> ".join(cyc))
    for tid, t in ids.items():
        if not prereqs.get(tid) and not t.get("root_reason"):
            err("%s: no prerequisites and no root_reason" % tid)
        if prereqs.get(tid) and t.get("root_reason"):
            warn("%s: has prerequisites but also root_reason" % tid)
    return prereqs


def check_questions(questions, ids):
    by_topic = {}
    qids = set()
    for q in questions:
        qid, tid = q.get("id", "?"), q.get("topicId")
        if tid not in ids:
            err("%s: unknown topic %s" % (qid, tid))
            continue
        if qid in qids:
            err("%s: duplicate question id" % qid)
        qids.add(qid)
        if not re.match(r"^%s_q\d+$" % re.escape(tid), qid):
            err("%s: id must be <topicId>_qN" % qid)
        by_topic.setdefault(tid, []).append(q)
        if q.get("difficulty") not in DIFF:
            err("%s: bad difficulty" % qid)
        if q.get("type") not in QTYPES:
            err("%s: bad type" % qid)
        for k in ("prompt", "answer", "explanation"):
            if not str(q.get(k, "")).strip():
                err("%s: empty %s" % (qid, k))
        if q.get("tech") not in (None, "free", "active"):
            err("%s: bad tech" % qid)
        if q.get("type") == "choice":
            ch = q.get("choices") or []
            keys = [c.get("key") for c in ch]
            if not (3 <= len(ch) <= 4) or keys != list("ABCD"[:len(ch)]):
                err("%s: choices must be 3-4 with keys A.." % qid)
            if len({c.get("text") for c in ch}) != len(ch):
                err("%s: duplicate choice text" % qid)
            if q.get("answer") not in keys:
                err("%s: answer %r is not a choice key" % (qid, q.get("answer")))
        if q.get("type") == "numeric" and not numeric_answer_ok(q.get("answer", "")):
            err("%s: numeric answer %r does not parse" % (qid, q.get("answer")))
    for tid, t in ids.items():
        qs = by_topic.get(tid, [])
        if len(qs) < 4:
            err("%s: has %d questions (need >= 4)" % (tid, len(qs)))
        if sum(1 for q in qs if q.get("difficulty") == "basic") < 2:
            err("%s: needs >= 2 basic questions" % tid)
        if t.get("tech") == "free" and sum(1 for q in qs if q.get("tech") != "active") < 2:
            err("%s: tech-free topic needs >= 2 tech-free questions" % tid)
    return by_topic


def main():
    quiet = "--quiet" in sys.argv
    std = load("standards.json")
    std_ids = {s["id"] for s in std}
    if len(std_ids) != len(std):
        err("standards.json: duplicate ids")
    topics = load("topics.json")
    deps = load("dependencies.json")
    questions = load("questions.json")
    ids = check_topics(topics, std_ids)
    prereqs = check_edges(deps, ids)
    check_questions(questions, ids)

    cited = {s["id"] for t in topics for s in t.get("standards", [])}
    if not quiet:
        by_band = {}
        for t in topics:
            by_band[t["band"]] = by_band.get(t["band"], 0) + 1
        hard = sum(1 for d in deps if d["strength"] == "hard")
        print("topics: %d %s" % (len(topics), by_band))
        print("edges: %d (hard %d, soft %d); roots: %d" % (
            len(deps), hard, len(deps) - hard, sum(1 for i in ids if not prereqs.get(i))))
        print("questions: %d" % len(questions))
        for fw in ("ac9", "ac9-optional", "qcaa2025"):
            items = [s for s in std if s["framework"] == fw and s.get("kind") != "unit"]
            n = sum(1 for s in items if s["id"] in cited)
            print("standards %-13s mapped %3d / %3d" % (fw, n, len(items)))
    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print("validate: %s (%d errors, %d warnings)" % ("FAIL" if errors else "OK", len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
