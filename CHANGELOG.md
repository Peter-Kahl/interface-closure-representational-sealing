# Changelog

All notable changes to this repository are recorded here.

## 1.1.0 — 2026-10-06

Adds Case 5, a leak, for §10.3 of Version 2.0 of the paper. Cases 1–4 are numerically unchanged: with the same seed and environment, every figure they print is identical to version 1.0.2.

- New Case 5 relaxes the sealing condition with a leak channel `X4`, whose response depends weakly on the realiser kind (`P(X4=1 | k1) = 0.505`, `P(X4=1 | k2) = 0.495`, so ε = 0.01). The response probabilities are fixed by the channel's mechanism, not fitted.
- Case 5 reports:
  - the discrimination profile D_N of the pair 'k1 fills the high-X1 state' versus 'k2 fills it', bracketed exactly by Hellinger bounds and estimated by Monte Carlo simulation of the optimal test;
  - the number of trials at which D_N can first reach 0.9 (reliability 95 per cent);
  - a fitted comparison of the two assignments on a reference dataset;
  - the worst-case error rate of that comparison over simulated datasets; and
  - an absorption check showing that a leak whose response is a free parameter transmits nothing.
- Case 5 uses its own seeded generator (`LEAK_RANDOM_SEED = 5`) and runs after Case 4, so it neither alters nor depends on Cases 1–4.
- Module documentation updated: five claims, the leak model, and the corresponding limitations and reproducibility notes.
- Reference output regenerated with Python 3.13.16 and NumPy 2.5.3. Compared with the 1.0.2 reference file, the only differences in Cases 1–4 are the version lines and, in Case 1, which example two-detector fits are printed, as documented in `README.md`.

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
