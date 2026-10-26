# Changelog

## 2026-10-26: Mathematical Methods Units 1–4

- Methods is complete: 93 topics across all 20 syllabus topics (Units 1–2 = Year 11, Units 3–4 = Year 12), 373 questions.
- 26 more Year 9, Year 10 and optional Year 10 topics that Methods depends on (Pythagoras, trigonometry, scientific notation, probability, exponentials, logarithms, polynomials, circles, unit circle, sine and cosine rules, standard deviation, box plots).
- Standards: Methods unit and topic titles confirmed against the official syllabus; 35 Methods sub-topics added (`qcaa25:MM.U#.T#.S#`), and every Methods topic maps to one.
- Verifier: numeric equality to 1e-12, sample-point fallback for trig/log identities, indefinite integrals compared up to a constant, `e`/`ln` in choices, `Phi()` and `binom_pmf()` helpers.
- Site: senior units show their school year, e.g. "Methods U3 (Year 12)".
- Tests: consistent-student tests for Unit 1, Unit 4 integration and Unit 4 statistics targets; smoke test covers a Year 12 diagnosis and unit screening.

## 2026-10-26: fork for Queensland (Year 9 to Year 12)

- Forked from cn-math-taxonomy at `cf262d8`. Removed the Chinese curriculum data, the English/Chinese/Physics subjects, child profiles, share images, PWA and stats.
- Kept the diagnosis algorithm in `diagnose/engine.js`. Translated it, replaced chapter parsing and level ranking (Year 9 → Unit 4), and rewrote answer judging for English input (`and`/`or`, `$`, metric units, named values).
- New data model: bands `y9`, `y10`, `y10opt`, `general`, `methods`, `specialist`; ids `qm_*`; `tech` field; `status: draft`.
- New `data/standards.json`: AC v9.0 Year 9–10 (paraphrased), optional post-Year 10 content (inferred), QCAA 2025 General/Methods/Specialist units and topics.
- New scripts: `standards_seed.py`, `build.py` (with transitive reduction), `validate.py` (level and track rules), `verify_questions.py` (SymPy), `blind_pass.py`, `ingest_mrac.py`.
- Pilot slice: 30 topics, 40 prerequisite links, 121 questions from Year 9 algebra to Methods Unit 1 Topic 1.
- New English UI: home, explore, diagnose. Engine tests and a Playwright smoke test.
