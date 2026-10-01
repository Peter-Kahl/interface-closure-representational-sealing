# Changelog

All notable changes to this repository are recorded here.

## 1.0.2 — 2026-09-30

Numerical behaviour is unchanged from 1.0.1: with the same seed, every figure is identical. Only labels and documentation changed.

- Latent state renamed from `G` to `S` throughout the code, comments and printed output, matching the paper, in which `G` denotes the condition inquired into.
- Case 3 renamed 'intervention without recoupling' in the printed output and documentation, matching the paper.
- Model description aligned with the paper: the realiser question is described as a structural parameter (an assignment of kinds to states), not as a cause of the latent state, and the sealing condition is stated as in §10.1.
- Reference output regenerated with Python 3.12.3 and NumPy 2.4.4.
- `LICENSE` copyright holder corrected to Peter Kahl.
- `CITATION.cff` updated to the paper's final title and series details; `requirements.txt`, `CHANGELOG.md` and `.zenodo.json` added.

## 1.0.1 — 2026-09-28

- Run configuration and each case now report the log-likelihood tolerances and the parameter-rounding convention used to count distinct solutions, on which §10.3 of the paper relies.
- Numerical results unchanged from 1.0.0.

## 1.0.0

- Initial version of the three-detector simulation.
