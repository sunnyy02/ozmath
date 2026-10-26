# QLD Maths Taxonomy (Year 9 to Year 12)

A prerequisite map of Queensland secondary maths with an adaptive diagnosis that finds the gap behind a student's struggle.

- **Map.** Topics from Australian Curriculum v9.0 Years 9 and 10, the optional post-Year 10 content, and the QCAA 2025 senior syllabuses (General, Methods and Specialist Mathematics). Each topic says which earlier topics it depends on (*hard* or *soft*, with a reason).
- **Question bank.** At least 4 questions per topic (at least 2 basic), machine-checked with SymPy where possible.
- **Diagnosis.** The student picks a target topic, unit or level. The tool asks at most 2 questions per topic. If they miss a topic twice, it works back through that topic's prerequisites until it finds where the gap starts, then gives a learning path in teaching order.

> **Status: draft.** Topics, prerequisites and questions were drafted with AI and have **not been reviewed by teachers**. Hard/soft judgements and some curriculum mappings are opinions. Please report problems with the issue templates.

This is a non-commercial fork of [cn-math-taxonomy](https://github.com/xiaoyang111222/cn-math-taxonomy) by xiaoyang111222, which does the same for the Chinese curriculum. The diagnosis algorithm (`diagnose/engine.js`) is theirs. Labels, level ordering and answer judging were adapted for QLD. Licence: CC BY-NC 4.0 (see `LICENSE`).

## Scope and progress

Senior subjects are organised by QCAA unit: Units 1–2 are taught in Year 11 and Units 3–4 in Year 12. The site labels them that way, e.g. "Methods U3 (Year 12)".

| Level | Curriculum | Topics | Questions | Status |
|---|---|---:|---:|---|
| Year 9 | AC v9.0 Year 9 | 15 | 60 | Topics that Methods depends on (number, algebra, measurement, probability) |
| Year 10 | AC v9.0 Year 10 | 11 | 44 | Topics that Methods depends on |
| Year 10 Optional | AC v9.0 optional content for post-Year 10 pathways | 14 | 56 | Surds, quadratics, logs, polynomials, unit circle, sine/cosine rules, standard deviation |
| Methods U1–U2 (Year 11) | QCAA Mathematical Methods 2025 | 51 | 205 | **Complete:** all 10 topics |
| Methods U3–U4 (Year 12) | QCAA Mathematical Methods 2025 | 42 | 168 | **Complete:** all 10 topics |
| General Mathematics | QCAA 2025, Units 1–4 | 0 | 0 | Not started (unit and topic titles loaded) |
| Specialist Mathematics | QCAA 2025, Units 1–4 | 0 | 0 | Not started (unit and topic titles loaded) |

Totals: 133 topics, 201 prerequisite links (150 hard, 51 soft), 533 questions. Every Methods topic maps to one of the 35 official Methods sub-topics. 454 answers are machine-checked with SymPy (0 mismatches); 79 are word or interval answers that need the blind pass. Years 7–8 and Essential Maths are out of scope; topics with no earlier topic carry a `root_reason`.

## Run it

```bash
python3 -m http.server 8000      # from the repo root
# open http://localhost:8000/
```

Useful links: `diagnose/?target=qm_m4_018&demo=1` (Year 12 demo with a simulated student), `diagnose/?scope=Methods%20U3` (screen a whole unit), `diagnose/?scope=Methods` (all four units), `explore/?band=methods#qm_m3_011`, `map/` (the whole graph; filter by level, click a topic to highlight its prerequisites and dependents).

## Build and check

```bash
python3 scripts/standards_seed.py    # data/standards.json (curriculum layer)
python3 scripts/build.py             # content scripts -> topics, dependencies, questions
python3 scripts/validate.py          # schema, DAG, level and track rules, coverage
python3 scripts/verify_questions.py  # SymPy answer check (pip install -r requirements-dev.txt)
node tests/test_engine.js            # diagnosis engine tests
node tests/smoke.js http://localhost:8000 screenshots   # browser smoke test (needs Playwright)
```

Current results: validate OK; verify 454 auto-verified, 0 mismatches, 79 without a machine check (left for the blind pass); a mutation test that corrupts every checked answer catches all of them; 16 engine tests pass (including a simulated student for every possible gap behind three Methods targets); browser smoke test passes.

## How it is organised

```
data/standards.json        AC v9.0 Year 9-10 content descriptions, optional content, QCAA unit/topic items
data/topics.json           topics (built)            data/dependencies.json   prerequisite links (built)
data/questions.json        question bank (built)     data/verification_report.json   SymPy results
scripts/content/*.py       the source of truth for topics, links and questions (one file per slice)
scripts/qlib.py            authoring helpers, level ranks, Unicode-maths -> SymPy
scripts/build.py           builds data/ from content, with transitive reduction
scripts/validate.py        all structural rules         scripts/verify_questions.py  SymPy answer check
scripts/blind_pass.py      independent re-solve workflow   scripts/ingest_mrac.py   official AC wording
diagnose/                  engine.js (algorithm) + app.js (UI)    explore/   topic browser and graph
map/                       the full graph, filterable by level
docs/                      sources, modelling guide, question format, roadmap
```

Read `docs/modelling-guide.md` before adding topics.

## Topic fields

| Field | Meaning |
|---|---|
| `id` | `qm_9_###`, `qm_10_###`, `qm_10o_###`, `qm_g{U}_###`, `qm_m{U}_###`, `qm_s{U}_###`. Never reused; renames go through `data/id-aliases.json` |
| `band`, `level`, `unit` | `y9`, `y10`, `y10opt`, `general`, `methods`, `specialist`; level 9–12; senior unit 1–4 |
| `chapter` | `Year 10 · Algebra` or `Methods U1 · T1 Surds and quadratic functions` |
| `type` | conceptual, procedural, reasoning, application, modelling |
| `mastery_criteria` | 2–4 observable statements |
| `standards` | `[{id, confidence: exact\|inferred}]`, ids from `data/standards.json` |
| `tech` | free, active or either (mirrors QCAA technology-free and technology-active papers) |
| `status` | `draft` until a teacher reviews it, then `reviewed` |
| `root_reason` | required when a topic has no prerequisites |

## Rules the validator enforces

- The graph is acyclic, and a prerequisite never comes later than its topic (Year 9 < Year 10 < Year 10 Optional < Unit 1 < … < Unit 4).
- **Track rules.** General may depend only on Years 9–10 (not the optional content). Methods may depend on Years 9–10 and the optional content. Specialist may also depend on Methods, but only at the same or an earlier unit.
- Every topic maps to a standard, has 4+ questions with 2+ basic, and tech-free topics have 2+ tech-free questions.

## Curriculum sources (and what is still unverified)

See `docs/sources.md`. In short: the Year 9–10 wording is a paraphrase until `scripts/ingest_mrac.py` is run on the official MRAC file; the optional-content list is inferred; Methods unit, topic and sub-topic titles are checked against the official syllabus, with paraphrased sub-topic summaries; General and Specialist sub-topics are not yet loaded.
