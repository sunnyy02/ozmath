# Curriculum sources

Checked 2026-10-26. Neither ACARA's site nor QCAA's could be downloaded from the build environment, so some items below are second-hand. Each item records its status in `data/standards.json`.

| Layer | Source | Status in this repo | To do |
|---|---|---|---|
| AC v9.0 Year 9 and Year 10 content descriptions (`AC9M9…`, `AC9M10…`) | QCAA *Comparison of AC v8.4 to v9.0* (Year 9, Year 10), June 2023 | Codes correct. Text is a **short paraphrase** (`verbatim: false`) | Download the Mathematics JSON-LD from ACARA's [Machine-Readable Australian Curriculum](https://www.australiancurriculum.edu.au/machine-readable-australian-curriculum) into `sources/` and run `python3 scripts/ingest_mrac.py sources/<file> --dry-run`, then without `--dry-run`. The script was written without a sample file, so check its counts |
| Optional content for post-Year 10 pathways | ACARA support resource (DOCX, no codes) | **Inferred list** with our own ids `acopt:*` | Read the DOCX and correct the list. v9.0 has no coded “10A” any more |
| QCAA General Mathematics 2025 | Syllabus v1.3 (Jan 2026) | Unit and topic titles, official | Add sub-topic bullets |
| QCAA Mathematical Methods 2025 | Official syllabus PDF (read 2026-10-26) | Unit, topic and all 35 sub-topic titles official, with notional hours. Sub-topic subject matter is a one-line **paraphrase** (`verbatim: false`) | Optionally load the individual subject-matter bullets verbatim |
| QCAA Specialist Mathematics 2025 | Syllabus v1.4 (Mar 2026) | Unit and topic titles, official | Add sub-topic bullets |
| Years 9–10 sequencing evidence | QCAA *AC v9 Maths Years 7–10 content description sequence* | Used informally for prerequisite links | Cite it per edge when reviewing |

## Licences

- ACARA curriculum content and QCAA syllabuses: check each organisation's terms of use before redistributing large verbatim extracts (both are generally CC BY 4.0 with exceptions). Record the outcome here.
- Upstream code and data: CC BY-NC 4.0, © xiaoyang111222. This fork is non-commercial and keeps the same licence.

## Queensland context

- QLD P–6 began implementing AC v9.0 English and Maths in 2025; Years 7–10 must be fully on v9.0 by the end of 2027 (QCAA memo 043/23).
- Senior: QCAA 2025 syllabuses for students completing in 2026 or later. Assessment for General/Methods/Specialist is IA1 problem-solving and modelling 20%, IA2 15%, IA3 15%, external exam 50%. Specialist must be taken with or after Methods.
