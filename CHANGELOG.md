# Changelog

## 2026-10-26: fork for Queensland (Year 9 to Year 12)

- Forked from cn-math-taxonomy at `cf262d8`. Removed the Chinese curriculum data, the English/Chinese/Physics subjects, child profiles, share images, PWA and stats.
- Kept the diagnosis algorithm in `diagnose/engine.js`. Translated it, replaced chapter parsing and level ranking (Year 9 → Unit 4), and rewrote answer judging for English input (`and`/`or`, `$`, metric units, named values).
- New data model: bands `y9`, `y10`, `y10opt`, `general`, `methods`, `specialist`; ids `qm_*`; `tech` field; `status: draft`.
- New `data/standards.json`: AC v9.0 Year 9–10 (paraphrased), optional post-Year 10 content (inferred), QCAA 2025 General/Methods/Specialist units and topics.
- New scripts: `standards_seed.py`, `build.py` (with transitive reduction), `validate.py` (level and track rules), `verify_questions.py` (SymPy), `blind_pass.py`, `ingest_mrac.py`.
- Pilot slice: 30 topics, 40 prerequisite links, 121 questions from Year 9 algebra to Methods Unit 1 Topic 1.
- New English UI: home, explore, diagnose. Engine tests and a Playwright smoke test.
