# Modelling guide

How to add topics, prerequisite links and questions so the diagnosis stays meaningful. Read this before editing `scripts/content/`.

## 1. Topic size

One topic is **one skill that one short question can test**, roughly 20–60 minutes of teaching. Split a curriculum item when a student could plausibly do one part and not the other.

- Too big: “Quadratic functions”. A student can factorise but not complete the square.
- Too small: “Expanding (x + a)(x + b) when a and b are both positive”. That is a question, not a topic.
- Right: “Completing the square”, “The discriminant and the number of real solutions”.

A content description or QCAA sub-topic usually becomes 1–4 topics.

## 2. Prerequisite links

A link `A needs B` means a student who cannot do B will struggle with A.

- **hard**: without B, A cannot be done (the quadratic formula needs simplifying surds for exact answers).
- **soft**: B helps a lot but is not a gate (simultaneous linear equations help with finding a quadratic's rule).
- Give a one-line reason a teacher can judge.
- Link only to **direct** prerequisites. `build.py` removes a soft link if another path exists, and a hard link if another all-hard path exists, and prints what it removed.
- Prerequisites never come from a later level, and the track rules apply (General must not need the optional Year 10 content or Methods; Specialist may need Methods only at the same or an earlier unit).
- The diagnosis backtracks hard links before soft ones, so mislabelled hard links cost students the most time. When unsure, use soft.

## 3. Questions

- At least 4 per topic, at least 2 `basic` (the second question after a miss is basic when possible). Add `standard`, and `advanced` only for genuine stretch.
- Prefer `numeric` and `choice` so answers mark themselves. Numeric answers must be plain numbers, fractions, lists (`3, -5` with `unordered=True`), points `(2, -5)` or named values `b=-2, c=1`.
- Choice distractors should come from real errors: sign slips, forgetting to divide by 2a, (a + b)² = a² + b², dividing by x and losing x = 0.
- Write maths in Unicode: `x²`, `√5`, `(−1 ± √3)/2`, `−3`. The verifier converts it to SymPy.
- Give every question a `verify` SymPy expression that **computes** the answer (not a literal). The verifier reports literals as `restated`.
- Explanations: 1–2 sentences showing the key step.
- Mark questions that need a calculator with `tech="active"`.

## 4. Worked examples

**Year 10.** `qm_10_004` Solving quadratic equations algebraically: hard on `qm_9_009` (null factor law) and `qm_10_003` (non-monic factorising), soft on `qm_10_002` (difference of two squares appears in some equations, but students can still factorise in other ways).

**Year 10 Optional → Methods.** `qm_m1_003` The discriminant with an unknown coefficient: hard on `qm_10o_006` (discriminant conditions) and `qm_10_006` (the condition becomes a linear inequality in k).

**General (example for the next slice).** A topic such as “Compound interest: future value” would be hard on a Year 9/10 percentage/growth topic and soft on Year 10 exponential relations, but never on `qm_10o_*` content.

## 5. Workflow

1. Edit or add a file in `scripts/content/` and list it in `CONTENT` in `scripts/build.py`.
2. `python3 scripts/build.py && python3 scripts/validate.py && python3 scripts/verify_questions.py && node tests/test_engine.js`
3. Run `python3 scripts/blind_pass.py prepare` and have someone who cannot see the answers solve the batches; `compare` and adjudicate each mismatch.
4. Open a pull request. A teacher sets `status: reviewed` on topics they have checked.
