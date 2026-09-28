# Interface Closure and Representational Sealing

Computational supplement to:

**Peter Kahl, ‘What Conceptual Change Cannot Recover: Interface Closure and Representational Sealing’ (2026).**

This repository contains simulations accompanying the paper's analysis of **interface closure** and **representational sealing**. The code illustrates the distinction between identifying a latent role-level structure and gaining epistemic access to structure that lies beyond the stipulated interface.

## Three-detector simulation

`three_detector.py` implements the toy model developed in §10 of the paper.

A binary latent role-level state \(G \in \{a,b\}\) generates conditionally independent observations through noisy binary detectors:

\[
G \rightarrow (X_1,X_2,X_3).
\]

The simulation examines four cases.

### 1. Two detectors

With only \(X_1\) and \(X_2\), the latent-class model is ordinarily non-identifiable. Multiple materially different parameterisations can fit the same observational distribution.

Multiple random EM initialisations are used to make this numerical multiplicity visible.

### 2. Three detectors

Adding a suitable third conditionally independent detector generically identifies the role-level latent structure, subject to permutation of the two latent-state labels.

The simulation therefore distinguishes:

\[
\text{role-level underidentification}
\]

from

\[
\text{ordinary latent-label symmetry}.
\]

### 3. Role-mediated intervention

The simulation then introduces a randomised intervention \(U\):

\[
U \rightarrow G \rightarrow (X_1,X_2,X_3).
\]

The intervention changes the probability of the latent role-level state and substantially enriches the available regime information.

It nevertheless introduces no direct measurement path to the stipulated role-exceeding property \(Q\).

The example therefore illustrates an important point developed in the paper: **intervention does not, merely by being intervention, escape an interface**. An intervention mediated entirely through the same role-level state may improve identification of that state without providing access to distinctions beyond it.

### 4. Conventional statistical anchor

Finally, the model stipulates

\[
P(X_1=1\mid G=a)=0.9.
\]

This removes the ordinary statistical label ambiguity by fixing an orientation of the latent model.

It does not introduce a new measurement path or independently identify a role-exceeding realiser.

The example therefore distinguishes:

\[
\text{role identification}
\neq
\text{statistical orientation}
\neq
\text{realiser identification}.
\]

## Interface interpretation

The conceptual architecture represented by the simulation is:

```text
role-exceeding realiser / property Q
                |
                v
         role-level state G
          /      |      \
         v       v       v
        X1      X2      X3
```

In the intervention case:

```text
         U ---> G ---> (X1, X2, X3)
```

There is deliberately no direct \(Q \rightarrow X_i\) measurement path.

This matters for interpretation. The simulation does **not** establish that a real system is interface-closed, that role-exceeding structure exists, or that such structure is physically unobservable. Those are substantive premises that must be independently defended in an application of the theory.

The simulation instead asks what follows **conditional on the stipulated interface architecture**.

## Statistical label symmetry and realiser permutation

Two different permutation claims must not be conflated.

**Statistical label symmetry** arises because the labels \(a\) and \(b\) assigned to latent classes are arbitrary. Exchanging

\[
(\pi,p,q)
\]

with

\[
(1-\pi,q,p)
\]

leaves the observational likelihood unchanged.

`three_detector.py` verifies this equality numerically.

**Realiser permutation** is a different claim. It concerns exchanging role-exceeding realisers while holding fixed everything available through the stipulated interface.

The simulation's likelihood does not directly demonstrate such a permutation because \(Q\) is deliberately absent from the likelihood. Rather, invariance with respect to role-exceeding structure follows from the stipulated interface: the simulated observational system contains no \(Q\)-sensitive path.

## What the simulation does not prove

The code is an illustration, not a proof of the mathematical or philosophical claims developed in the paper.

In particular:

- numerical convergence from multiple EM initialisations does not prove global identifiability;
- observing multiple near-optimal two-detector fits does not establish the mathematical structure of the non-identifiable solution set;
- generic identifiability of the three-indicator latent-class model depends on mathematical results and their assumptions, not on this simulation;
- expectation-maximisation is a local optimisation procedure;
- finite-sample estimates need not equal the population parameters used to generate the data;
- statistical label symmetry is not itself evidence of role-exceeding realiser permutation; and
- a role-mediated intervention does not establish that every possible intervention would remain behind the interface.

The relevant identifiability literature, including Kruskal (1977) and Allman, Matias and Rhodes (2009), is discussed in the accompanying paper.

## Requirements

The simulation requires Python 3 and NumPy.

A minimal installation is:

```bash
python -m venv .venv
source .venv/bin/activate
pip install numpy
```

The code has no external data dependencies.

## Running the simulation

Run:

```bash
python three_detector.py
```

The script reports:

1. distinct near-optimal fits obtained with two detectors;
2. the two label-equivalent solutions recovered with three detectors;
3. the corresponding solutions under a role-mediated intervention;
4. the single statistical orientation obtained after conventional anchoring; and
5. a direct numerical check of likelihood invariance under latent-label exchange.

A fixed pseudo-random seed is used for reproducibility. Small numerical differences may nevertheless occur across Python, NumPy, platform, or numerical-library versions.

## Reproducibility

The generating parameters and random seed are defined explicitly in `three_detector.py`.

The canonical simulation uses:

```text
random seed = 1
N = 20,000
P(G=a) = 0.30

P(Xj=1 | G=a) = [0.90, 0.80, 0.85]
P(Xj=1 | G=b) = [0.20, 0.10, 0.30]
```

For the intervention:

```text
P(G=a | U=0) = 0.20
P(G=a | U=1) = 0.80
```

Each reported model is fitted from 40 random EM initialisations.

## Associated paper

Peter Kahl, **‘What Conceptual Change Cannot Recover: Interface Closure and Representational Sealing’** (2026).

Publication and DOI details will be added when available.

## Citation

If you use the theoretical argument, please cite the accompanying paper.

If you use or modify the software, please also cite the archived software release. Citation metadata are provided in `CITATION.cff`.

## Licence

The source code in this repository is released under the **MIT License**. See `LICENSE`.

The accompanying scholarly paper is a separate work and is licensed under **CC BY 4.0**, unless otherwise stated.

## Author

**Peter Kahl**  
Independent researcher, Lex et Ratio  
ORCID: 0009-0003-1616-4843  
[Lex et Ratio](https://www.lexetratio.com/?utm_source=chatgpt.com)