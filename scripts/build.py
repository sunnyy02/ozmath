#!/usr/bin/env python3
"""Rebuild data/topics.json, data/dependencies.json and data/questions.json from scripts/content/.

Every content module exposes a list T of (topic, deps, questions) tuples made with qlib.topic().
Modules are loaded in CONTENT order; topic order in the output is the authoring order.

Transitive reduction (same rule as the upstream cn-math-taxonomy):
  * a soft edge A->B is dropped if A can reach B by any other path;
  * a hard edge A->B is dropped only if A can reach B by another path made only of hard edges.
Dropped edges are printed so authors can tidy the content script.

Run:  python3 scripts/build.py
"""
import importlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "content"))

CONTENT = [
    "pilot_quadratics",
]


def reachable(start, goal, adj, skip_edge, hard_only):
    stack, seen = [start], {start}
    while stack:
        n = stack.pop()
        for p, strength in adj.get(n, []):
            if (n, p) == skip_edge:
                continue
            if hard_only and strength != "hard":
                continue
            if p == goal:
                return True
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return False


def reduce_edges(deps):
    adj = {}
    for d in deps:
        adj.setdefault(d["topicId"], []).append((d["prerequisiteId"], d["strength"]))
    kept, dropped = [], []
    for d in deps:
        e = (d["topicId"], d["prerequisiteId"])
        if reachable(d["topicId"], d["prerequisiteId"], adj, e, hard_only=(d["strength"] == "hard")):
            dropped.append(d)
            adj[d["topicId"]] = [x for x in adj[d["topicId"]] if x[0] != d["prerequisiteId"]]
        else:
            kept.append(d)
    return kept, dropped


def dump(name, obj):
    path = os.path.join(ROOT, "data", name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return path


def main():
    topics, deps, questions = [], [], []
    for mod in CONTENT:
        m = importlib.import_module(mod)
        for t, d, q in m.T:
            topics.append(t)
            deps.extend(d)
            questions.extend(q)
    kept, dropped = reduce_edges(deps)
    for d in dropped:
        print("reduced: %s -> %s (%s) is implied by another path" % (d["topicId"], d["prerequisiteId"], d["strength"]))
    dump("topics.json", topics)
    dump("dependencies.json", kept)
    dump("questions.json", questions)
    print("built %d topics, %d edges (%d reduced), %d questions" % (len(topics), len(kept), len(dropped), len(questions)))


if __name__ == "__main__":
    main()
