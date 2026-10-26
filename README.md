# QLD Maths Taxonomy (Year 9 to Year 12)

A prerequisite map of Queensland secondary maths with an adaptive diagnosis that finds the gap behind a student's struggle.

- **Map.** Topics from Australian Curriculum v9.0 Years 9 and 10, the optional post-Year 10 content, and the QCAA 2025 senior syllabuses (General, Methods and Specialist Mathematics). Each topic says which earlier topics it depends on (*hard* or *soft*, with a reason).
- **Question bank.** At least 4 questions per topic (at least 2 basic), machine-checked with SymPy where possible.
- **Diagnosis.** The student picks a target topic, unit or level. The tool asks at most 2 questions per topic. If they miss a topic twice, it works back through that topic's prerequisites until it finds where the gap starts, then gives a learning path in teaching order.

> **Status: draft.** Topics, prerequisites and questions were drafted with AI and have **not been reviewed by teachers**. Hard/soft judgements and some curriculum mappings are opinions. Please report problems with the issue templates.

This is a non-commercial fork of [cn-math-taxonomy](https://github.com/xiaoyang111222/cn-math-taxonomy) by xiaoyang111222, which does the same for the Chinese curriculum. The diagnosis algorithm (`diagnose/engine.js`) is theirs. Labels, level ordering and answer judging were adapted for QLD. Licence: CC BY-NC 4.0 (see `LICENSE`).

## Scope and progress

| Level | Curriculum | Topics | Questions | Status |
|---|---|---:|---:|---|
| Year 9 | AC v9.0 Year 9 | 10 | 40 | Pilot: Number and Algebra only |
| Year 10 | AC v9.0 Year 10 | 6 | 24 | Pilot: Algebra only |
| Year 10 Optional | AC v9.0 optional content for post-Year 10 pathways | 7 | 28 | Pilot: surds and quadratics |
| General Mathematics | QCAA 2025, Units 1–4 | 0 | 0 | Standards loaded at topic level |
| Mathematical Methods | QCAA 2025, Units 1–4 | 7 | 29 | Pilot: Unit 1 Topic 1 (Surds and quadratic functions) |
| Specialist Mathematics | QCAA 2025, Units 1–4 | 0 | 0 | Standards loaded at topic level |

The pilot slice runs from Year 9 algebra to Methods Unit 1 Topic 1. It has 30 topics, 40 prerequisite links and 121 questions. The aim was to prove the whole pipeline (content → validation → verification → site) before scaling up. Essential Mathematics and Years 7–8 are out of scope for now; Year 9 topics with no earlier topic carry a `root_reason`.

## Run it

```bash
python3 -m http.server 8000      # from the repo root
# open http://localhost:8000/
```

Useful links: `diagnose/?target=qm_m1_007&demo=1` (demo with a simulated student), `diagnose/?scope=Year%2010` (screen a whole level), `explore/#qm_10o_005`.

## Build and check

```bash
python3 scripts/standards_seed.py    # data/standards.json (curriculum layer)
python3 scripts/build.py             # content scripts -> topics, dependencies, questions
python3 scripts/validate.py          # schema, DAG, level and track rules, coverage
python3 scripts/verify_questions.py  # SymPy answer check (pip install -r requirements-dev.txt)
node tests/test_engine.js            # diagnosis engine tests
node tests/smoke.js http://localhost:8000 screenshots   # browser smoke test (needs Playwright)
```

Current results: validate OK; verify 109 auto-verified, 0 mismatches, 12 without a machine check (word answers or inequalities, left for the blind pass); 14 engine tests pass; smoke test passes.

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

See `docs/sources.md`. In short: the Year 9–10 wording is a paraphrase until `scripts/ingest_mrac.py` is run on the official MRAC file; the optional-content list is inferred; Methods topic titles come from a third-party summary; QCAA sub-topic bullet points are not yet loaded.
