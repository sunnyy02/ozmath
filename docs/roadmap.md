# Roadmap

Follows the implementation plan (Phases 0–7). Done so far: Phases 0–1, the pilot slice, and Mathematical Methods Units 1–4.

| Phase | Status |
|---|---|
| 0 Setup: fork, English rewrite, validator, CI-ready scripts, issue templates | Done |
| 1 Standards layer | Partly done: AC Year 9–10 codes (paraphrased text), optional content (inferred), QCAA unit/topic titles, Methods sub-topics (official titles). Still to do: run `ingest_mrac.py` on the official file; add General and Specialist sub-topics; check the optional-content list |
| Pilot slice: Year 9 algebra → Methods U1 T1 | Done: 30 topics, 40 links, 121 questions, 109 SymPy-verified |
| 2 Year 9–10 graph (all strands) | Partly done: the 40 Year 9–10 topics Methods depends on. Remaining strands (e.g. geometry, measurement, statistics investigations) not started |
| 3 Senior graphs (General, Methods, Specialist) | Methods complete (Units 1–4: 93 topics, 373 questions, plus 26 Year 9–10 topics it depends on). General and Specialist not started |
| 4 Full question bank + blind pass | Not started (tooling ready) |
| 5 Site | Core done (home, explore, diagnose, results, export, print). Not ported from upstream: child profiles, share image, PWA/offline, usage stats |
| 6 Teacher review and pilot | Not started |
| 7 Extensions (Essential Maths, textbook/C2C mappings, difficulty calibration) | Not started |

## Known gaps

- 9 root topics (Year 9 entry points, Year 10 inequalities and box plots) stand in for Years 7–8, which are out of scope.
- 79 questions have no machine check (word answers, inequalities, intervals, interpretations) and need the blind pass.
- Methods IA1 (problem-solving and modelling task) is not diagnosable with short questions and is not modelled.
- Some Methods probability and statistics topics (sampling, interpretation of intervals) rely on choice questions only.
