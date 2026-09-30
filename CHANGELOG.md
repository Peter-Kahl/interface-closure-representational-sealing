# Changelog

All notable changes to this repository are recorded here.

## Documentation revision — 2026-09-30

Code behaviour and output are unchanged; `three_detector.py` remains version 1.0.1.

- Model description aligned with the published paper. The realiser question is now described as a structural parameter (an assignment of kinds to states), not as a cause of the latent state, and the sealing condition is stated as in §10.1 of the paper.
- Notation correspondence added: the code's `G` is the paper's `S`.
- Case 3 renamed 'intervention without recoupling', matching the paper.
- `LICENSE` copyright holder corrected to Peter Kahl.
- `CITATION.cff` updated to the paper's final title and series details; `requirements.txt`, `CHANGELOG.md` and `.zenodo.json` added.
- README records an independent reproduction and notes which parts of the output may vary across environments.

## 1.0.1 — 2026-09-28

- Run configuration and each case now report the log-likelihood tolerances and the parameter-rounding convention used to count distinct solutions, on which §10.3 of the paper relies.
- Numerical results unchanged from 1.0.0.

## 1.0.0

- Initial version of the three-detector simulation.
