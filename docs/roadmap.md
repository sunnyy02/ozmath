# Roadmap

Follows the implementation plan (Phases 0–7). Done in this fork so far: Phases 0–1 and a pilot slice.

| Phase | Status |
|---|---|
| 0 Setup: fork, English rewrite, validator, CI-ready scripts, issue templates | Done |
| 1 Standards layer | Partly done: AC Year 9–10 codes (paraphrased text), optional content (inferred), QCAA unit/topic titles. Still to do: run `ingest_mrac.py` on the official file; add QCAA sub-topic bullets; check Methods titles and the optional-content list |
| Pilot slice: Year 9 algebra → Methods U1 T1 | Done: 30 topics, 40 links, 121 questions, 109 SymPy-verified |
| 2 Year 9–10 graph (all strands) | Next. Checkpoint A: teacher review of structure before writing questions |
| 3 Senior graphs (General, Methods, Specialist) | Not started |
| 4 Full question bank + blind pass | Not started (tooling ready) |
| 5 Site | Core done (home, explore, diagnose, results, export, print). Not ported from upstream: child profiles, share image, PWA/offline, usage stats |
| 6 Teacher review and pilot | Not started |
| 7 Extensions (Essential Maths, textbook/C2C mappings, difficulty calibration) | Not started |

## Known gaps in the pilot

- Year 9 roots (`qm_9_001`, `qm_9_002`, `qm_9_004`, `qm_9_007`, `qm_9_008`) and `qm_10_006` stand in for Years 7–8, which are out of scope.
- 12 questions have no machine check (word answers, inequalities, graph descriptions) and need the blind pass.
- Methods U1 T1 topics map to the topic as a whole (`inferred`) because sub-topic bullets are not loaded.
