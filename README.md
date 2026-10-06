# Interface Closure and Representational Sealing

<p align="left">
  <img
    src="assets/representational-sealing-2.jpg"
    alt="Representational sealing: heterogeneous role-exceeding structure is mediated through an interface into a restricted observable representation."
  >
</p>

Computational supplement to:

**Peter Kahl, ‘What Conceptual Change Cannot Recover: Interface Closure, Epistemic Recoupling and Representational Sealing’ (2026). Lex et Ratio Working Paper LXR-2026-PHI-RESTCERT-WP, Version 2.0. doi: 10.5281/zenodo.23086003.**

This repository contains the simulation accompanying the paper's toy model of **interface closure** and **representational sealing** (§10). The code illustrates the difference between identifying a latent role-level structure and gaining access to structure that the stipulated interface does not transmit. From version 1.1.0 it also illustrates the paper's quantitative extension (§5.7): a weak leak, its **discrimination profile**, and the difference between a distinction that is untransmitted and one that is transmitted but certification-infeasible within a given amount of inquiry.

It also contains the complete console output of the reference run reported in §10.3 of the paper, so that the numerical claims can be inspected without rerunning the simulation.

## Notation

The code follows the paper's notation: the latent role-level state is `S`, and `G` (in the paper) denotes the condition inquired into.

## The model

A binary latent state `S ∈ {a, b}` generates conditionally independent readings through three noisy binary detectors:

```text
S → (X1, X2, X3)
```

The target's two states are realised by two kinds, which differ in a property `Q`. Which kind fills which state is **not** a variable in the model. In the paper it is a structural parameter: an assignment `α` of kinds to states. The sealing condition is

```text
P(X1, X2, X3 | S; α) = P(X1, X2, X3 | S)   for every assignment α
```

Given the state, the readings do not depend on which kind realises it. In Cases 1–4 the code implements this condition by construction: neither `α` nor `Q` appears anywhere in the simulation or the likelihood, so there is no `Q`-sensitive measurement path. Case 5 relaxes the condition (below).

This matters for interpretation. The simulation does **not** establish that a real system is interface-closed, that role-exceeding structure exists, or that such structure is physically unobservable. Those are substantive premises that must be independently defended when the theory is applied. The simulation shows what follows **conditional on the stipulated interface**.

## The five cases

### 1. Two detectors

With only `X1` and `X2`, the latent-class model is not identifiable: the observed two-detector distribution has three independent degrees of freedom, while the model has five free parameters. Many materially different parameterisations fit the same observations, and repeated EM (expectation-maximisation) runs from random starting points make this visible.

The result is illustrative. The finite set of solutions the program finds does not itself establish the mathematical structure of the non-identifiable solution set.

### 2. Three detectors

Adding a third suitable conditionally independent detector generically identifies the role-level structure up to relabelling of the two latent states (Kruskal 1977; Allman, Matias and Rhodes 2009). The simulation recovers one role-level structure in its two label orientations.

This case removes ordinary statistical non-identifiability, so that what remains undetermined is visibly the assignment of realiser kinds to states.

### 3. Intervention without recoupling

A randomised intervention `U` changes the probability of the latent state:

```text
U → S → (X1, X2, X3)
```

The intervention enriches the available observations, but acts only through the same state. It introduces no path sensitive to `Q`, and the two label orientations remain.

> **Intervening defeats a seal only if it acts through a dependence sensitive to the sealed distinction.**

An intervention confined to the same interface may improve identification of the state without giving access to distinctions beyond it. A different intervention or measurement that produced a `Q`-sensitive response would change the situation: in the paper's terms it would be a *refining recoupling*, which lies outside the model.

### 4. A stipulated response probability

Finally, the model is fitted with the stipulation

```text
P(X1=1 | S=a) = 0.9
```

This removes the statistical label ambiguity by fixing which latent state is *called* `a`. It answers a naming question:

```text
Which latent component is designated a?
```

It does not answer a different one:

```text
Which independently specified realiser kind occupies that position?
```

It adds no measurement path and no information about `Q`.

### 5. A leak

Case 5 relaxes the sealing condition. A fourth reading, the leak channel `X4`, responds weakly to the kind that realises the current state:

```text
P(X4=1 | kind k1) = (1 + ε)/2 = 0.505
P(X4=1 | kind k2) = (1 − ε)/2 = 0.495        (ε = 0.01)

S → (X1, X2, X3)        (S, α) → X4
```

The two response probabilities are treated as fixed by the channel's mechanism, as Requirement 5.1 of the paper demands. At ε = 0 the channel is a fair coin and the model is sealed again.

The case compares two interpretations with the generating role-level parameters: *k1 fills the high-X1 state* and *k2 fills it*. One trial, in which all four readings are taken, counts as one step sensitive for this pair. It reports:

1. **The discrimination profile** D_N: the best total variation distance any procedure can achieve between the two interpretations' distributions over N trials. It is bracketed exactly by Hellinger bounds and estimated by Monte Carlo simulation of the optimal (likelihood-ratio) test.
2. **The trials needed** for D_N to reach 0.9, which reliable discrimination at 95 per cent requires.
3. **A fitted comparison** of the two assignments on a reference dataset of 20,000 trials, with the role-level parameters estimated.
4. **The worst-case error rate** of that comparison over simulated datasets, at 20,000 and 100,000 trials.
5. **An absorption check.** If the leak channel's response probabilities were free parameters of the fitted model, the two assignments would produce the same distribution of records. The leak would then be absorbed, and the assignment would be untransmitted.

At 20,000 trials the profile is below 0.9, so the assignment is **transmitted but certification-infeasible** at that amount of inquiry; with enough trials it becomes reliably discriminable. The absorption check shows why the calibration of the leak channel matters: a leak counts as transmission only if how the channel responds to each kind is fixed independently of the fit.

## Label symmetry and realiser permutation

Two permutation claims must not be conflated.

**Statistical label symmetry.** The labels `a` and `b` are arbitrary. Exchanging `(pi, p, q)` with `(1-pi, q, p)` leaves the likelihood unchanged, and `three_detector.py` checks this numerically. This symmetry is an invariance of the model's likelihood.

**Realiser permutation.** Exchanging which kind realises which state is a different claim. It concerns a distinction the likelihood does not parameterise at all. Its invariance follows, within the toy model, from the stipulated interface, not from anything the likelihood shows.

```text
statistical label symmetry  ≠  realiser permutation
```

## What the simulation does not show

The code is an illustration, not a proof of the paper's mathematical or philosophical claims. In particular:

- convergence from multiple EM starts does not prove global identifiability;
- the multiple near-optimal two-detector fits do not establish the structure of the non-identifiable solution set;
- generic identifiability of the three-indicator model rests on mathematical results and their assumptions, not on this simulation;
- EM is a local optimisation method and may converge to local optima or numerically distinct approximations;
- finite-sample estimates need not equal the generating parameters;
- statistical label symmetry is not evidence of realiser permutation;
- an intervention acting through the state does not show that every possible intervention would remain behind the interface;
- Case 5's leak is a stipulated toy mechanism, and a small ε is a small statistical distance, not a small physical flux; and
- the simulation does not establish interface closure in any real physical, computational, biological or social system.

## Requirements

- Python 3.8 or later
- NumPy 1.17 or later (see `requirements.txt`)

No external data files are needed: the observations are generated internally from the parameters and random seed set in the source code.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the simulation

```bash
python three_detector.py
```

The script reports:

1. the distinct near-optimal fits obtained with two detectors;
2. the two label-equivalent solutions recovered with three detectors;
3. the corresponding solutions under intervention without recoupling;
4. the single orientation obtained under the stipulation;
5. the leak case: discrimination profile, trials needed, fitted comparison, error rates and absorption check; and
6. a numerical check of likelihood invariance under exchange of latent-state labels.

## Reference output

`output/three_detector_output.txt` is the complete, unedited console output of the reference run reported in §10.3 of the paper, produced by `three_detector.py` version **1.1.0** with Python 3.13.16 and NumPy 2.5.3.

It is provided for reproducibility and scrutiny. It is not an independent empirical dataset: the observations are simulated by the program itself.

To compare a new run with it:

```bash
python three_detector.py > my_run.txt
diff -u output/three_detector_output.txt my_run.txt
```

**Reproduction across environments.** Version 1.0.1, which differs from 1.0.2 only in its labels (see `CHANGELOG.md`), was run with Python 3.14.7 and NumPy 2.5.3. Every figure the paper reports was identical to the reference run: the count of 36 near-optimal two-detector solutions, both three-detector solutions and their log-likelihoods, the intervention and stipulation cases, and the label-swap check. The only difference was among the four *example* two-detector fits printed under Case 1. These are drawn from a nearly flat likelihood, so which examples are printed first can vary between environments. The paper does not rely on them.

Version 1.1.0 leaves every figure of Cases 1–4 unchanged from version 1.0.2. Its Case 5 uses its own seeded generator, so its figures do not depend on the earlier cases.

In general, exact textual identity is not guaranteed across Python, NumPy or platform versions, and small floating-point differences do not by themselves indicate a failure to reproduce. Case 5's Monte Carlo estimates are reported with their standard errors.

## Reproducibility

The generating parameters and random seed are set explicitly in `three_detector.py`:

```text
random seed = 1
N = 20,000

P(S=a) = 0.30
P(Xj=1 | S=a) = [0.90, 0.80, 0.85]
P(Xj=1 | S=b) = [0.20, 0.10, 0.30]
```

For the intervention:

```text
P(S=a | U=0) = 0.20
P(S=a | U=1) = 0.80
```

For the leak (Case 5):

```text
leak random seed = 5
ε = 0.01
reliability 1 − δ = 0.95, so reliable discrimination needs D_N ≥ 0.9
profile reported at N = 1,000; 5,000; 10,000; 20,000; 50,000; 100,000
Monte Carlo replications per profile value = 20,000
fitted-comparison replications = 200 per truth and per N (N = 20,000; 100,000)
```

Cases 1–4 are each fitted from 40 random EM starts. Fits within 0.01 (two detectors) or 0.001 (three detectors) of the best log-likelihood are counted, and parameters are rounded to two decimal places to identify distinct solutions. The rounding is a reporting convention, not a mathematical criterion of distinctness.

Cases 1–4 share one seeded random-number generator, so changing an earlier case changes the data and starting points of later ones. Case 5 has its own. Exact reproduction therefore requires the same script version as well as the same seed.

## Expected qualitative results

| Case | Expected result |
|---|---|
| Two detectors | Many distinct near-optimal parameterisations |
| Three detectors | One role-level structure in two label orientations |
| Intervention without recoupling | Richer information about the state, but the two label orientations remain |
| Stipulated response probability | One statistical orientation |
| A leak | Profile below 0.9 at 20,000 trials and above it with enough trials; fitted comparison unreliable at 20,000 trials; absorption check exact |
| Label-swap check | Equal likelihoods up to floating-point error |

## Repository structure

```text
interface-closure-representational-sealing/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── CITATION.cff
├── .zenodo.json
├── .gitignore
├── requirements.txt
├── three_detector.py
├── output/
│   └── three_detector_output.txt
└── assets/
    └── representational-sealing-2.jpg
```

## Version correspondence

The numerical results in §10.3 of Version 2.0 of the paper correspond to `three_detector.py` **version 1.1.0**. Those in Version 1.0 of the paper correspond to version 1.0.2, whose figures for Cases 1–4 are unchanged. Use the archived release of that version when reproducing or citing those results. Later versions may produce different output. See `CHANGELOG.md` for the history of changes.

## Citation

If you use the theoretical argument, please cite the paper:

> Kahl, P. (2026) *What Conceptual Change Cannot Recover: Interface Closure, Epistemic Recoupling and Representational Sealing*. Lex et Ratio Working Paper LXR-2026-PHI-RESTCERT-WP, Version 2.0. doi: 10.5281/zenodo.23086003.

If you use or modify the software, please also cite the archived software release. Citation metadata are in `CITATION.cff`. The paper and the software are separate scholarly objects with separate persistent identifiers.

## Licence

The source code is released under the **MIT License** (see `LICENSE`). The accompanying paper is a separate work, licensed under **CC BY 4.0**.

## Disclaimer

This software supports reproducibility and scrutiny of the accompanying theoretical argument. Its output should be read together with the assumptions, definitions, limitations and argument of the paper. It is not, by itself, evidence of representational sealing or interface closure in any real-world system.

The software is provided ‘as is’, without warranty of any kind, as specified in the MIT License.

## Author

**Peter Kahl**\
Independent researcher, Lex et Ratio\
ORCID: [0009-0003-1616-4843](https://orcid.org/0009-0003-1616-4843)\
[www.lexetratio.com](https://www.lexetratio.com)