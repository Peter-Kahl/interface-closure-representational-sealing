#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
three_detector.py
=================

Version:
    1.1.0 (2026-10-06)

Supplementary research code for:

    Peter Kahl, "What Conceptual Change Cannot Recover:
    Interface Closure, Epistemic Recoupling and Representational
    Sealing" (2026), Version 2.0,
    §10, "A toy model of sealing: three detectors", and §5.7,
    "Approximate closure and discrimination profiles".

Author:
    Peter Kahl
    Independent researcher, Lex et Ratio
    https://www.lexetratio.com
    ORCID: 0009-0003-1616-4843

Repository:
    GitHub: https://github.com/Peter-Kahl/interface-closure-representational-sealing

Copyright:
    Copyright (c) 2026 Peter Kahl

Licence:
    MIT License

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

    This licence applies to the source code in this repository. The associated
    paper is a separate scholarly work and is licensed under CC BY 4.0 unless
    otherwise stated.

Purpose
-------
This script supplies the numerical illustration discussed in §10.3 of the
paper. It simulates a binary latent target state S in {a, b} observed through
conditionally independent noisy binary detectors. It then fits latent-class
models by expectation-maximisation (EM) from multiple random initialisations.

The script illustrates five claims made in §10:

    1. With only two detectors, the role-level statistical structure is
       ordinarily non-identifiable: multiple distinct near-optimal parameter
       solutions can fit the same observed distribution.

    2. With three suitable conditionally independent detectors, the role-level
       structure is generically identifiable up to permutation of the two
       latent-state labels.

    3. Intervention without recoupling: adding an intervention whose
       influence is mediated entirely through the same role-level state
       enriches the observational regime but does not, by itself, attach an
       independently specified realiser kind to either latent state or break
       a permutation of role-exceeding realisers. Intervening defeats a seal
       only if it acts through a dependence sensitive to the sealed
       distinction.

    4. Fixing P(X1=1 | S=a)=0.9 breaks the statistical label symmetry by
       stipulation. It fixes which latent position is called 'a'; it does not
       establish which role-exceeding realiser occupies that position.

    5. A leak: if the sealing condition is relaxed by a weak channel whose
       response to each realiser kind is fixed by its mechanism, the
       assignment of kinds is transmitted, but only weakly. Its
       discrimination profile (§5.7) can be computed, and at the sample size
       of the other cases it lies below what reliable discrimination
       requires: the assignment is transmitted but certification-infeasible
       at that amount of inquiry. The case also shows that a leak whose
       response to the kinds is a free parameter of the fitted model is
       absorbed by that parameter, and transmits nothing.

Interface interpretation
------------------------
Notation. The latent role-level state is written S, as in the paper, where S
denotes the condition inquired into.

The paper distinguishes the causal interface from the architectural factor
derived from it. In this toy model, every detector and intervention accessible
to the simulated layer depends on the target only through the role-level
state:

             S ---> (X1, X2, X3)

and, in the intervention case:

    U ---> S ---> (X1, X2, X3)

Which realiser kind fills which state is not a variable in this model. In the
paper it is a structural parameter: an assignment alpha of kinds to states,
where the kinds differ in a property Q. The sealing condition is

    P(X1, X2, X3 | S; alpha) = P(X1, X2, X3 | S)   for every assignment alpha:

given the state, the readings do not depend on which kind realises it. In
Cases 1-4 the code implements this condition by construction: neither alpha
nor Q appears anywhere in the simulation or the likelihood. There is no
Q-sensitive measurement path.

Case 5 relaxes the condition. It adds a fourth reading X4, a leak channel,
whose response depends weakly on the kind that realises the current state:

    P(X4=1 | kind k1) = (1 + epsilon) / 2
    P(X4=1 | kind k2) = (1 - epsilon) / 2

These two probabilities are treated as fixed by the leak channel's mechanism,
as Requirement 5.1 of the paper demands, not fitted. At epsilon = 0 the
channel is a fair coin and the model is sealed again. Because the kind that
fills the current state is fixed by the assignment alpha and the state S
together, X4 depends on alpha:

    S, alpha ---> X4        S ---> (X1, X2, X3)

The simulation therefore does NOT establish that any real system is
interface-closed, that role-exceeding structure exists, or that such structure
is physically unobservable. Those are substantive premises that must be
independently justified when applying the theory. The code illustrates the
statistical consequences conditional on the stipulated interface.

Two different permutation claims must be kept separate:

    * statistical label symmetry: exchanging the names a and b in the fitted
      latent-class model while transforming all associated parameters; and

    * realiser permutation: exchanging role-exceeding realisers while holding
      fixed everything available through the stipulated interface.

The likelihood calculation directly demonstrates only the first. The second
follows, within the toy model, from the stipulated interface closure: Q is not
itself represented in the likelihood.

Methodological limitations
--------------------------
This program is an illustrative simulation, not a mathematical proof,
empirical validation, or demonstration that the model describes any particular
physical, biological, computational, or social system.

In particular:

    * numerical convergence from multiple EM initialisations does not prove
      global identifiability;

    * observing multiple near-optimal two-detector fits does not prove that
      the population-level non-identifiable solution set is continuous;

    * the generic identifiability claim for the three-indicator latent-class
      model depends on mathematical results and their assumptions, not on this
      simulation alone;

    * EM is a local optimisation procedure and can converge to local optima,
      saddle points, or numerically distinct approximations;

    * finite-sample estimates need not equal the population parameters used to
      generate the data;

    * statistical label symmetry must not be conflated with permutation of
      role-exceeding realisers;

    * intervention through S does not test whether some different intervention
      or measurement could breach the stipulated interface;

    * Case 5's discrimination profile is computed at the grain of whole
      trials: one trial, in which all four readings are taken, counts as one
      step sensitive for the pair compared. The profile is bracketed exactly
      by Hellinger-distance bounds and estimated by Monte Carlo simulation;
      the Monte Carlo estimate carries the sampling error it reports;

    * Case 5's leak is a stipulated toy mechanism. A small value of epsilon
      is a small statistical distance, not a small physical flux (§5.7 of the
      paper); and

    * Case 1 uses a near-optimal log-likelihood tolerance of 1e-2, whereas the
      three-detector cases use 1e-3. The looser tolerance is deliberate: the
      two-detector model is non-identifiable and has a flat or nearly flat
      likelihood region, so numerically distinct EM solutions can differ
      slightly in finite-iteration log-likelihood while illustrating the same
      underlying non-identifiability. The three-detector cases use the tighter
      tolerance to identify solutions converging on the discrete near-best
      label orientations.

For reporting purposes, fitted solutions are classified as distinct after
rounding the prior and detector parameters to two decimal places. This is a
display and deduplication convention only; it is not a mathematical criterion
of distinctness and does not alter the fitted parameter values or likelihoods.

The relevant mathematical identifiability results are discussed and cited in
the accompanying paper, including Kruskal (1977) and Allman, Matias and Rhodes
(2009).

Reproducibility
---------------
The simulation uses a fixed pseudo-random seed and reports the Python and
NumPy versions used at runtime, together with the numerical likelihood
tolerances used to classify fitted solutions. Results should therefore be
reproducible with a compatible NumPy environment, subject to ordinary
differences in numerical libraries, floating-point arithmetic, platform,
software versions, and pseudo-random number generation behaviour.

Because Cases 1-4 share one pseudo-random generator, changing the order or
number of random draws in an earlier case can change the generated data or EM
initialisations in later cases even when RANDOM_SEED is unchanged. Exact
reproduction therefore requires the same script version as well as the same
seed and compatible software environment.

Case 5 uses its own generator, seeded with LEAK_RANDOM_SEED, and runs after
Case 4. Adding it leaves every figure of Cases 1-4 unchanged from version
1.0.2, and its own figures do not depend on the earlier cases.

No external data files are required.

Research-use disclaimer
-----------------------
This software is provided to support reproducibility and scrutiny of the
accompanying theoretical argument. Its outputs should be interpreted together
with the assumptions, definitions, limitations, and argument of the paper.

The numerical output is not, by itself, evidence for the existence of
representational sealing in any real-world system.
"""

from __future__ import annotations

import sys

import numpy as np


# ---------------------------------------------------------------------------
# Script version, reproducibility, and simulation constants
# ---------------------------------------------------------------------------

SCRIPT_VERSION = "1.1.0"

RANDOM_SEED = 1
N_TRIALS = 20_000
N_STARTS = 40
EM_ITERATIONS_3 = 500
EM_ITERATIONS_2 = 800

# Case 1 deliberately uses a looser tolerance because the two-detector model
# is non-identifiable and its likelihood can be flat or nearly flat across
# numerically distinct parameterisations. The three-detector cases use the
# tighter tolerance to isolate the discrete near-best label orientations.
LIKELIHOOD_TOLERANCE_2 = 1e-2
LIKELIHOOD_TOLERANCE_3 = 1e-3

# Fitted solutions are classified as distinct for reporting purposes after
# rounding the prior and detector parameters to this many decimal places.
# This is a display/deduplication convention, not a mathematical criterion
# of distinctness.
SOLUTION_KEY_DECIMALS = 2

rng = np.random.default_rng(RANDOM_SEED)

# Generating role-level parameters used in §10.3.
TRUE_PI = 0.30
TRUE_P = np.array([0.90, 0.80, 0.85], dtype=float)  # P(Xj=1 | S=a)
TRUE_Q = np.array([0.20, 0.10, 0.30], dtype=float)  # P(Xj=1 | S=b)

# Intervention parameters: P(S=a | U=0), P(S=a | U=1).
TRUE_R = np.array([0.20, 0.80], dtype=float)

# Case 5 (a leak). The leak channel X4 reads 1 with probability
# (1 + LEAK_EPSILON) / 2 when the current state is realised by kind k1, and
# (1 - LEAK_EPSILON) / 2 when it is realised by kind k2. These probabilities
# are fixed by the channel's mechanism and are not fitted.
LEAK_EPSILON = 0.01

# Case 5 uses its own generator, so that Cases 1-4 are unchanged from
# version 1.0.2 and Case 5 does not depend on them.
LEAK_RANDOM_SEED = 5

# Reliability at which settling is assessed: worst-case success probability
# 1 - delta. Reliable discrimination of a pair requires D_N >= 1 - 2 delta.
LEAK_DELTA = 0.05

# Numbers of trials N at which the discrimination profile is reported.
LEAK_PROFILE_N = (1_000, 5_000, 10_000, 20_000, 50_000, 100_000)

# Monte Carlo replications used to estimate each profile value.
LEAK_MC_REPLICATIONS = 20_000

# Simulated datasets per truth and per N for the fitted test's error rates.
LEAK_TEST_REPLICATIONS = 200
LEAK_TEST_N = (20_000, 100_000)

# EM settings for the leak model (fitted on cell counts).
LEAK_EM_STARTS = 8
LEAK_EM_ITERATIONS = 500


def validate_intervention(
    u: np.ndarray,
    n: int,
) -> np.ndarray:
    """
    Validate and return a binary intervention vector.

    The intervention must contain exactly one value per trial, all values must
    be 0 or 1, and both intervention conditions must be represented. Requiring
    both conditions prevents undefined group means in the intervention EM
    update.
    """
    u = np.asarray(u)

    if u.ndim != 1:
        raise ValueError("u must be a one-dimensional intervention vector.")

    if len(u) != n:
        raise ValueError("u must contain one intervention value per trial.")

    if not np.all(np.isin(u, [0, 1])):
        raise ValueError("u must contain only 0 and 1.")

    if not (np.any(u == 0) and np.any(u == 1)):
        raise ValueError(
            "u must contain observations in both intervention groups."
        )

    return u.astype(int, copy=False)


def simulate(
    n: int,
    pi: float | None,
    p: np.ndarray,
    q: np.ndarray,
    *,
    u: np.ndarray | None = None,
    r: np.ndarray | None = None,
) -> np.ndarray:
    """Simulate detector readings from the binary latent-state model."""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)

    if p.shape != q.shape:
        raise ValueError("p and q must have the same shape.")

    if u is None:
        if pi is None:
            raise ValueError("pi is required for passive simulation.")
        prob_a = np.full(n, float(pi))
    else:
        if r is None:
            raise ValueError("r is required when an intervention u is supplied.")

        u = validate_intervention(u, n)
        r = np.asarray(r, dtype=float)

        if r.shape != (2,):
            raise ValueError(
                "r must contain exactly two intervention probabilities."
            )

        prob_a = np.where(u == 1, r[1], r[0])

    # True denotes the role-level state S=a.
    s_is_a = rng.random(n) < prob_a

    x = np.empty((n, len(p)), dtype=int)

    for j in range(len(p)):
        draw_if_a = rng.random(n) < p[j]
        draw_if_b = rng.random(n) < q[j]
        x[:, j] = np.where(s_is_a, draw_if_a, draw_if_b)

    return x


def loglik_and_posterior(
    x: np.ndarray,
    prob_a: float | np.ndarray,
    p: np.ndarray,
    q: np.ndarray,
) -> tuple[float, np.ndarray]:
    """Compute observed-data log-likelihood and posterior P(S=a | record)."""
    likelihood_a = (
        np.prod(np.where(x == 1, p, 1.0 - p), axis=1) * prob_a
    )
    likelihood_b = (
        np.prod(np.where(x == 1, q, 1.0 - q), axis=1) * (1.0 - prob_a)
    )
    total = likelihood_a + likelihood_b

    if np.any(total <= 0.0):
        raise FloatingPointError("Encountered a zero or negative likelihood.")

    return float(np.log(total).sum()), likelihood_a / total


def fit_three_detector_em(
    x: np.ndarray,
    *,
    u: np.ndarray | None = None,
    fixed_p0: float | None = None,
    iterations: int = EM_ITERATIONS_3,
) -> tuple[float, float | np.ndarray, np.ndarray, np.ndarray]:
    """Fit the latent binary model by EM for three-detector records."""
    m = x.shape[1]

    p = rng.uniform(0.05, 0.95, m)
    q = rng.uniform(0.05, 0.95, m)

    if u is None:
        pi = float(rng.uniform(0.05, 0.95))
    else:
        u = validate_intervention(u, len(x))
        r = rng.uniform(0.05, 0.95, 2)

    if fixed_p0 is not None:
        p[0] = fixed_p0

    for _ in range(iterations):
        prob_a = pi if u is None else np.where(u == 1, r[1], r[0])
        _, weight_a = loglik_and_posterior(x, prob_a, p, q)

        if u is None:
            pi = float(weight_a.mean())
        else:
            r = np.array(
                [
                    weight_a[u == 0].mean(),
                    weight_a[u == 1].mean(),
                ]
            )

        p = (weight_a[:, None] * x).sum(axis=0) / weight_a.sum()

        q = (
            ((1.0 - weight_a)[:, None] * x).sum(axis=0)
            / (1.0 - weight_a).sum()
        )

        if fixed_p0 is not None:
            p[0] = fixed_p0

    prob_a = pi if u is None else np.where(u == 1, r[1], r[0])
    log_likelihood, _ = loglik_and_posterior(x, prob_a, p, q)
    prior = pi if u is None else r

    return log_likelihood, prior, p, q


def fit_two_detector_em(
    x: np.ndarray,
    *,
    iterations: int = EM_ITERATIONS_2,
) -> tuple[float, float, np.ndarray, np.ndarray]:
    """Fit the passive two-detector latent binary model by EM."""
    if x.shape[1] != 2:
        raise ValueError("fit_two_detector_em expects exactly two detectors.")

    p = rng.uniform(0.05, 0.95, 2)
    q = rng.uniform(0.05, 0.95, 2)
    pi = float(rng.uniform(0.05, 0.95))

    for _ in range(iterations):
        _, weight_a = loglik_and_posterior(x, pi, p, q)

        pi = float(weight_a.mean())

        p = (
            (weight_a[:, None] * x).sum(axis=0)
            / weight_a.sum()
        )

        q = (
            ((1.0 - weight_a)[:, None] * x).sum(axis=0)
            / (1.0 - weight_a).sum()
        )

    log_likelihood, _ = loglik_and_posterior(x, pi, p, q)

    return log_likelihood, pi, p, q


def parameter_key(
    prior: float | np.ndarray,
    p: np.ndarray,
    q: np.ndarray,
    *,
    decimals: int = SOLUTION_KEY_DECIMALS,
) -> tuple[float, ...]:
    """
    Produce a rounded key used to classify numerically distinct displayed fits.

    The rounding convention is used only for reporting and deduplication. It
    does not alter fitted parameters, likelihoods, or the underlying model.
    """
    values = np.concatenate(
        [
            np.atleast_1d(prior),
            p,
            q,
        ]
    )

    return tuple(float(v) for v in np.round(values, decimals))


def format_vector(
    values: np.ndarray,
    decimals: int = 3,
) -> str:
    """Format a parameter vector without NumPy scalar representations."""
    return (
        "["
        + ", ".join(f"{float(v):.{decimals}f}" for v in values)
        + "]"
    )


def format_two_detector_solution(
    prior: float,
    p: np.ndarray,
    q: np.ndarray,
    *,
    decimals: int = 3,
) -> str:
    """Format one two-detector solution in a clean human-readable form."""
    return (
        f"prior={prior:.{decimals}f}  "
        f"p={format_vector(p, decimals)}  "
        f"q={format_vector(q, decimals)}"
    )


def report_three_detector_fits(
    name: str,
    fits: list[
        tuple[
            float,
            float | np.ndarray,
            np.ndarray,
            np.ndarray,
        ]
    ],
    *,
    likelihood_tolerance: float = LIKELIHOOD_TOLERANCE_3,
) -> None:
    """
    Print rounded-distinct near-best three-detector solutions.

    Fits within the specified log-likelihood tolerance are classified as
    distinct for reporting after parameter rounding by parameter_key().
    """
    fits = sorted(fits, key=lambda fit: -fit[0])

    best = fits[0][0]
    seen: set[tuple[float, ...]] = set()
    displayed = 0

    print(f"\n=== {name} ===")

    for log_likelihood, prior, p, q in fits:
        if best - log_likelihood > likelihood_tolerance:
            continue

        key = parameter_key(prior, p, q)

        if key in seen:
            continue

        seen.add(key)
        displayed += 1

        prior_text = (
            f"{float(prior):.3f}"
            if np.ndim(prior) == 0
            else format_vector(np.asarray(prior), 3)
        )

        print(
            f"loglik={log_likelihood:.4f}  "
            f"prior={prior_text}  "
            f"p={format_vector(p, 3)}  "
            f"q={format_vector(q, 3)}"
        )

    print(
        "distinct near-best solutions "
        f"(Δloglik <= {likelihood_tolerance:g}; "
        f"parameters rounded to {SOLUTION_KEY_DECIMALS} d.p.) "
        f"found among {len(fits)} starts: {displayed}"
    )


def report_run_configuration() -> None:
    """Print the software environment and fixed simulation configuration."""
    print("=== Run configuration ===")
    print(f"script version = {SCRIPT_VERSION}")
    print(f"Python version = {sys.version.split()[0]}")
    print(f"NumPy version = {np.__version__}")
    print(f"random seed = {RANDOM_SEED}")
    print(f"N = {N_TRIALS}")
    print(f"P(S=a) = {TRUE_PI}")
    print(f"P(Xj=1 | S=a) = {format_vector(TRUE_P, 2)}")
    print(f"P(Xj=1 | S=b) = {format_vector(TRUE_Q, 2)}")
    print(f"EM random starts per case = {N_STARTS}")
    print(
        "log-likelihood tolerances: "
        f"two-detector={LIKELIHOOD_TOLERANCE_2:g}, "
        f"three-detector={LIKELIHOOD_TOLERANCE_3:g}"
    )
    print(
        "solution-key rounding for reporting = "
        f"{SOLUTION_KEY_DECIMALS} decimal places"
    )


def run_case_1_two_detectors(
    x_three: np.ndarray,
) -> None:
    """
    Case 1: fit only X1 and X2.

    The model is ordinarily non-identifiable at the role level. The finite
    collection of solutions encountered here illustrates that fact; it does
    not numerically prove the existence or geometry of the population-level
    non-identifiable solution set.

    A looser likelihood tolerance is used here than in the three-detector
    cases because the non-identifiable model can have a flat or nearly flat
    likelihood region. Numerically distinct EM fits may therefore differ
    slightly in finite-iteration likelihood while illustrating the same
    underlying non-identifiability.

    Distinctness in the reported count is operationalised by rounding the
    fitted prior and detector parameters to SOLUTION_KEY_DECIMALS decimal
    places. This is a reporting convention, not a claim that the resulting
    classes are mathematically distinct solutions.
    """
    fits = [
        fit_two_detector_em(x_three[:, :2])
        for _ in range(N_STARTS)
    ]

    fits.sort(key=lambda fit: -fit[0])
    best = fits[0][0]

    # Retain one representative fit for each rounded reporting key.
    representatives: dict[
        tuple[float, ...],
        tuple[
            float,
            float,
            np.ndarray,
            np.ndarray,
        ],
    ] = {}

    for fit in fits:
        if best - fit[0] > LIKELIHOOD_TOLERANCE_2:
            continue

        key = parameter_key(
            fit[1],
            fit[2],
            fit[3],
        )

        representatives.setdefault(key, fit)

    print("\n=== Case 1. two detectors ===")

    print(
        "distinct near-optimal solutions "
        f"(Δloglik <= {LIKELIHOOD_TOLERANCE_2:g}; "
        f"parameters rounded to {SOLUTION_KEY_DECIMALS} d.p.) "
        f"found among {N_STARTS} starts: {len(representatives)}"
    )

    print(
        "(The underlying two-indicator model is non-identifiable; "
        "the finite set reported here is only a numerical illustration.)"
    )

    for fit in list(representatives.values())[:4]:
        _, prior, p, q = fit

        print(
            "  "
            + format_two_detector_solution(
                prior,
                p,
                q,
            )
        )


def run_case_2_three_detectors(
    x_three: np.ndarray,
) -> None:
    """
    Case 2: fit all three passive detectors.

    For generic parameter values the role-level model is identifiable up to
    permutation of the two latent-state labels. Multiple EM starts should
    therefore recover the same role structure in the two label orientations,
    subject to finite-sample and optimisation variation.
    """
    fits = [
        fit_three_detector_em(x_three)
        for _ in range(N_STARTS)
    ]

    report_three_detector_fits(
        "Case 2. three detectors",
        fits,
    )


def run_case_3_intervention() -> None:
    """
    Case 3: intervention without recoupling. Add a randomised intervention U
    whose effect is mediated by S.

    U changes P(S=a) across intervention conditions, enriching the role-level
    observational structure. Because U reaches the detectors only through S,
    it introduces no direct Q-sensitive path. It therefore does not, by
    itself, identify a role-exceeding realiser or break a permutation of such
    realisers behind the stipulated interface.
    """
    u = rng.integers(
        0,
        2,
        N_TRIALS,
    )

    x = simulate(
        N_TRIALS,
        None,
        TRUE_P,
        TRUE_Q,
        u=u,
        r=TRUE_R,
    )

    fits = [
        fit_three_detector_em(
            x,
            u=u,
        )
        for _ in range(N_STARTS)
    ]

    report_three_detector_fits(
        "Case 3. three detectors + intervention without recoupling",
        fits,
    )

    print(
        "The intervention changes the role-level prior but remains mediated "
        "through S; it supplies no direct Q-sensitive observation and "
        "therefore does not break realiser permutation behind the stipulated "
        "interface."
    )


def run_case_4_stipulation(
    x_three: np.ndarray,
) -> None:
    """
    Case 4: stipulate P(X1=1 | S=a)=0.9.

    This is a conventional/statistical anchor. It selects an orientation of
    the latent statistical model and thereby removes ordinary label switching
    in the fit. It is not a target-side anchor: no independently specified
    role-exceeding realiser is measured, and the causal interface is unchanged.
    """
    fits = [
        fit_three_detector_em(
            x_three,
            fixed_p0=0.90,
        )
        for _ in range(N_STARTS)
    ]

    report_three_detector_fits(
        "Case 4. conventional stipulation P(X1=1 | S=a)=0.9",
        fits,
    )

    print(
        "The stipulation fixes a statistical orientation only; it is not a "
        "target-side anchor and does not add a new measurement path."
    )

# ---------------------------------------------------------------------------
# Case 5: a leak
# ---------------------------------------------------------------------------

# The 16 possible records (X1, X2, X3, X4) of one trial, in a fixed order.
LEAK_CELLS = np.array(
    [
        [(c >> 3) & 1, (c >> 2) & 1, (c >> 1) & 1, c & 1]
        for c in range(16)
    ],
    dtype=int,
)


def leak_channel_probabilities(
    k1_fills_a: bool,
    epsilon: float = LEAK_EPSILON,
) -> tuple[float, float]:
    """
    Return P(X4=1 | S=a) and P(X4=1 | S=b) under an assignment of kinds.

    The leak channel responds to the kind realising the current state, not to
    the state as such. Which kind realises which state is fixed by the
    assignment: if k1 fills a, k2 fills b, and conversely.
    """
    k1_response = (1.0 + epsilon) / 2.0
    k2_response = (1.0 - epsilon) / 2.0

    if k1_fills_a:
        return k1_response, k2_response

    return k2_response, k1_response


def leak_cell_distribution(
    pi: float,
    p: np.ndarray,
    q: np.ndarray,
    k1_fills_a: bool,
    *,
    epsilon: float = LEAK_EPSILON,
) -> np.ndarray:
    """Probability of each of the 16 trial records under the leak model."""
    c_a, c_b = leak_channel_probabilities(k1_fills_a, epsilon)

    p_all = np.append(np.asarray(p, dtype=float), c_a)
    q_all = np.append(np.asarray(q, dtype=float), c_b)

    likelihood_a = (
        np.prod(np.where(LEAK_CELLS == 1, p_all, 1.0 - p_all), axis=1) * pi
    )
    likelihood_b = (
        np.prod(np.where(LEAK_CELLS == 1, q_all, 1.0 - q_all), axis=1)
        * (1.0 - pi)
    )

    return likelihood_a + likelihood_b


def fit_leak_em_on_counts(
    counts: np.ndarray,
    generator: np.random.Generator,
    *,
    epsilon: float = LEAK_EPSILON,
    starts: int = LEAK_EM_STARTS,
    iterations: int = LEAK_EM_ITERATIONS,
) -> dict[bool, tuple[float, float, np.ndarray, np.ndarray]]:
    """
    Fit the leak model by EM on cell counts, under both assignments.

    The role-level parameters (pi, p, q) are free; the leak channel's response
    to each kind is fixed. EM is run with the leak channel's k1 response
    attached to state a. A converged fit in which detector 1 reads 1 more
    often in state a than in state b places k1 in the high-X1 state; a fit
    with the opposite orientation is the same model with the state labels
    exchanged, and places k2 there.

    Returns, for each hypothesis h ('k1 fills the high-X1 state' is True),
    the best fit (log-likelihood, pi, p, q) in the orientation in which state
    a is the high-X1 state. Starts are run in vectorised batches until both
    hypotheses have at least one fit.
    """
    counts = np.asarray(counts, dtype=float)
    c_a, c_b = leak_channel_probabilities(True, epsilon)
    x = LEAK_CELLS[:, :3]
    x4 = LEAK_CELLS[:, 3]

    leak_a = np.where(x4 == 1, c_a, 1.0 - c_a)
    leak_b = np.where(x4 == 1, c_b, 1.0 - c_b)

    best: dict[bool, tuple[float, float, np.ndarray, np.ndarray]] = {}

    for _batch in range(10):
        pi = generator.uniform(0.05, 0.95, starts)
        p = generator.uniform(0.05, 0.95, (starts, 3))
        q = generator.uniform(0.05, 0.95, (starts, 3))

        for _ in range(iterations):
            like_a = (
                np.prod(
                    np.where(x[None, :, :] == 1, p[:, None, :],
                             1.0 - p[:, None, :]),
                    axis=2,
                )
                * leak_a[None, :]
                * pi[:, None]
            )
            like_b = (
                np.prod(
                    np.where(x[None, :, :] == 1, q[:, None, :],
                             1.0 - q[:, None, :]),
                    axis=2,
                )
                * leak_b[None, :]
                * (1.0 - pi[:, None])
            )
            weight_a = like_a / (like_a + like_b)

            mass_a = (counts[None, :] * weight_a).sum(axis=1)
            mass_b = counts.sum() - mass_a

            pi = mass_a / counts.sum()
            p = (counts[None, :, None] * weight_a[:, :, None]
                 * x[None, :, :]).sum(axis=1) / mass_a[:, None]
            q = (counts[None, :, None] * (1.0 - weight_a)[:, :, None]
                 * x[None, :, :]).sum(axis=1) / mass_b[:, None]

        for i in range(starts):
            # Compute each final likelihood in the orientation in which
            # state a is the high-X1 state.
            k1_in_high_state = bool(p[i, 0] > q[i, 0])

            if k1_in_high_state:
                fit_pi, fit_p, fit_q = float(pi[i]), p[i], q[i]
            else:
                fit_pi, fit_p, fit_q = 1.0 - float(pi[i]), q[i], p[i]

            cell_prob = leak_cell_distribution(
                fit_pi, fit_p, fit_q, k1_in_high_state, epsilon=epsilon
            )
            log_likelihood = float((counts * np.log(cell_prob)).sum())

            current = best.get(k1_in_high_state)
            if current is None or log_likelihood > current[0]:
                best[k1_in_high_state] = (
                    log_likelihood, fit_pi, fit_p.copy(), fit_q.copy()
                )

        if True in best and False in best:
            return best

    raise RuntimeError(
        "EM did not produce fits for both assignments; increase starts."
    )


def smallest_n_reaching(
    bhattacharyya: float,
    target: float,
    *,
    upper_bound: bool,
) -> int:
    """
    Smallest N at which a Hellinger bound on D_N reaches the target.

    For N independent trials, the Bhattacharyya coefficient of the N-trial
    distributions is BC**N, and

        1 - BC**N  <=  D_N  <=  sqrt(1 - BC**(2N)).

    With upper_bound=True, return the smallest N at which the upper bound
    reaches the target: below it, D_N is certainly below the target. With
    upper_bound=False, return the smallest N at which the lower bound
    reaches it: from there on, D_N is certainly at least the target.
    """
    log_bc = np.log(bhattacharyya)

    if upper_bound:
        n = np.log(1.0 - target**2) / (2.0 * log_bc)
    else:
        n = np.log(1.0 - target) / log_bc

    return int(np.ceil(n - 1e-9))


def run_case_5_leak() -> None:
    """
    Case 5: a leak. Relax the sealing condition by a weak channel X4 whose
    response to each realiser kind is fixed by its mechanism.

    The pair compared is theta (k1 fills the high-X1 state) and theta'
    (k2 fills it), with the generating role-level parameters. One trial is
    one step, sensitive for the pair. The case reports:

        (a) the per-trial distance and the discrimination profile D_N,
            bracketed exactly by Hellinger bounds and estimated by Monte
            Carlo simulation of the optimal (likelihood-ratio) test;

        (b) the number of trials at which D_N can first reach 1 - 2 delta;

        (c) the generalised likelihood-ratio comparison of the two
            assignments on a reference dataset of N_TRIALS trials, with the
            role-level parameters fitted;

        (d) the worst-case error rate of the fitted comparison over
            simulated datasets; and

        (e) an absorption check: if the leak channel's response to the kinds
            were a free parameter, the two assignments would fit equally well.
    """
    generator = np.random.default_rng(LEAK_RANDOM_SEED)
    target = 1.0 - 2.0 * LEAK_DELTA

    print(f"\n=== Case 5. a leak (epsilon = {LEAK_EPSILON:g}) ===")
    print(
        "leak channel X4: P(X4=1 | k1) = "
        f"{(1.0 + LEAK_EPSILON) / 2.0:.3f}, P(X4=1 | k2) = "
        f"{(1.0 - LEAK_EPSILON) / 2.0:.3f} (fixed by mechanism, not fitted)"
    )
    print(
        "pair compared: k1 fills the high-X1 state vs k2 fills it; "
        "role-level parameters as generated; one trial = one sensitive step"
    )
    print(
        f"leak random seed = {LEAK_RANDOM_SEED}; reliability 1 - delta = "
        f"{1.0 - LEAK_DELTA:g}, so reliable discrimination needs "
        f"D_N >= {target:g}"
    )

    p_theta = leak_cell_distribution(TRUE_PI, TRUE_P, TRUE_Q, True)
    p_theta_prime = leak_cell_distribution(TRUE_PI, TRUE_P, TRUE_Q, False)

    per_trial_tv = 0.5 * float(np.abs(p_theta - p_theta_prime).sum())
    bhattacharyya = float(np.sqrt(p_theta * p_theta_prime).sum())
    log_ratio = np.log(p_theta / p_theta_prime)

    # (a) Profile.
    print("\n(a) discrimination profile")
    print(f"per-trial total variation distance = {per_trial_tv:.6f}")
    print(f"per-trial Bhattacharyya coefficient = {bhattacharyya:.9f}")
    print(
        "        N   Hellinger lower   Monte Carlo D_N (s.e.)   "
        "Hellinger upper"
    )

    for n in LEAK_PROFILE_N:
        lower = 1.0 - bhattacharyya**n
        upper = float(np.sqrt(1.0 - bhattacharyya ** (2 * n)))

        # D_N = E_theta[(1 - P_theta'/P_theta)_+] over N-trial records;
        # the cell counts are sufficient.
        counts = generator.multinomial(
            n, p_theta, size=LEAK_MC_REPLICATIONS
        )
        log_lr = counts @ log_ratio
        terms = np.clip(1.0 - np.exp(-log_lr), 0.0, None)
        estimate = float(terms.mean())
        standard_error = float(terms.std(ddof=1) / np.sqrt(len(terms)))

        print(
            f"{n:>9,}   {lower:15.4f}   {estimate:12.4f} ({standard_error:.4f})"
            f"   {upper:15.4f}"
        )

    print(
        f"(Monte Carlo: {LEAK_MC_REPLICATIONS:,} simulated N-trial records "
        "per row, each scored by the optimal likelihood-ratio test.)"
    )

    # (b) Thresholds.
    n_necessary = smallest_n_reaching(bhattacharyya, target, upper_bound=True)
    n_sufficient = smallest_n_reaching(
        bhattacharyya, target, upper_bound=False
    )
    n_linear = int(np.ceil(target / per_trial_tv))

    print(f"\n(b) trials needed for D_N >= {target:g}")
    print(
        f"per-trial TV bound (Corollary 5.2): at least {n_linear:,} trials "
        "(far from tight: the leak is a two-sided shift, §5.7)"
    )
    print(f"Hellinger upper bound: at least {n_necessary:,} trials")
    print(f"Hellinger lower bound: at most {n_sufficient:,} trials")
    print(
        f"At N = {N_TRIALS:,}, D_N < {target:g}: within that many trials the "
        "assignment is certification-infeasible at this reliability, though "
        "it is transmitted (X1-X3 generically identify the role structure, "
        "and X4's calibrated response then fixes the assignment)."
    )

    # (c) Reference dataset.
    reference_counts = generator.multinomial(N_TRIALS, p_theta)
    fits = fit_leak_em_on_counts(reference_counts, generator)
    ll_k1, pi_k1, p_k1, q_k1 = fits[True]
    ll_k2, pi_k2, p_k2, q_k2 = fits[False]
    difference = ll_k1 - ll_k2
    oracle = float(reference_counts @ log_ratio)

    print(
        f"\n(c) reference dataset: N = {N_TRIALS:,} trials generated with "
        "k1 filling the high-X1 state"
    )
    print(
        f"k1 fills high-X1 state: loglik={ll_k1:.4f}  prior={pi_k1:.3f}  "
        f"p={format_vector(p_k1, 3)}  q={format_vector(q_k1, 3)}"
    )
    print(
        f"k2 fills high-X1 state: loglik={ll_k2:.4f}  prior={pi_k2:.3f}  "
        f"p={format_vector(p_k2, 3)}  q={format_vector(q_k2, 3)}"
    )
    print(
        f"fitted log-likelihood ratio (k1 vs k2) = {difference:.4f}; "
        f"with equal prior odds, P(k1 fills high-X1 state | data) = "
        f"{1.0 / (1.0 + np.exp(-difference)):.3f}"
    )
    print(
        "log-likelihood ratio with the role-level parameters known "
        f"= {oracle:.4f}"
    )

    # (d) Error rates of the fitted comparison.
    print(
        "\n(d) fitted comparison over simulated datasets "
        f"({LEAK_TEST_REPLICATIONS} per truth and per N)"
    )

    for n in LEAK_TEST_N:
        error_rates = []

        for truth_k1, cell_prob in ((True, p_theta), (False, p_theta_prime)):
            errors = 0

            for _ in range(LEAK_TEST_REPLICATIONS):
                counts = generator.multinomial(n, cell_prob)
                fitted = fit_leak_em_on_counts(counts, generator)
                verdict_k1 = fitted[True][0] > fitted[False][0]
                errors += int(verdict_k1 != truth_k1)

            error_rates.append(errors / LEAK_TEST_REPLICATIONS)

        print(
            f"N = {n:>7,}: error rate when k1 fills high-X1 state = "
            f"{error_rates[0]:.3f}; when k2 does = {error_rates[1]:.3f}; "
            f"worst case = {max(error_rates):.3f}"
        )

    # (e) Absorption check.
    c_a, c_b = leak_channel_probabilities(True)
    absorbed = leak_cell_distribution(
        TRUE_PI, TRUE_P, TRUE_Q, False, epsilon=-LEAK_EPSILON
    )
    ll_calibrated = float(reference_counts @ np.log(p_theta))
    ll_absorbed = float(reference_counts @ np.log(absorbed))

    print("\n(e) absorption check")
    print(
        "If the leak channel's responses were free parameters, then "
        "'k1 fills the high-X1 state, with P(X4=1) = "
        f"{c_a:.3f} there and {c_b:.3f} in the other state' and "
        "'k2 fills it, with the same response probabilities' would give the "
        "same distribution of records:"
    )
    print(
        f"loglik, k1 with calibrated responses = {ll_calibrated:.6f}\n"
        f"loglik, k2 with exchanged responses  = {ll_absorbed:.6f}\n"
        f"difference                          = "
        f"{abs(ll_calibrated - ll_absorbed):.12g}"
    )
    print(
        "A leak transmits the assignment only because the channel's response "
        "to each kind is fixed independently of the fit (Requirement 5.1). "
        "Absorbed by a free parameter, it leaves the pair transmission-"
        "equivalent and the assignment untransmitted."
    )


def report_label_swap_invariance(
    x_three: np.ndarray,
) -> None:
    """
    Verify likelihood invariance under permutation of latent-state labels.

    Swapping a <-> b requires simultaneously replacing pi by 1-pi and
    exchanging p with q. The resulting likelihood equality demonstrates
    statistical label redundancy. It must not be conflated with realiser
    permutation: role-exceeding realisers are absent from this likelihood.
    """
    loglik_original, _ = loglik_and_posterior(
        x_three,
        TRUE_PI,
        TRUE_P,
        TRUE_Q,
    )

    loglik_swapped, _ = loglik_and_posterior(
        x_three,
        1.0 - TRUE_PI,
        TRUE_Q,
        TRUE_P,
    )

    difference = abs(
        loglik_original - loglik_swapped
    )

    print("\n=== Label-swap invariance check ===")

    print(
        f"original loglik = {loglik_original:.6f}\n"
        f"swapped  loglik = {loglik_swapped:.6f}\n"
        f"difference       = {difference:.12g}"
    )

    print(
        "Any non-zero difference at this scale is floating-point error. "
        "This check concerns statistical label symmetry only; realiser "
        "permutation is a distinct interface-level claim."
    )


def main() -> None:
    """
    Run the complete §10.3 supplementary simulation in textual order.

    The passive three-detector dataset is generated once and reused for
    Cases 1, 2 and 4. Case 3 requires a separate dataset because it introduces
    the intervention U. Case 5 generates its own data, with its own seeded
    generator, because it adds the leak channel X4.

    All random draws in Cases 1-4 use the same seeded NumPy generator.
    Consequently, the exact Case 3 data and later EM initialisations depend on
    the sequence of random draws made by earlier cases. Exact numerical reproduction therefore
    requires the same script version as well as a compatible software
    environment.
    """
    report_run_configuration()

    passive_x = simulate(
        N_TRIALS,
        TRUE_PI,
        TRUE_P,
        TRUE_Q,
    )

    # Order follows §10.3 of the paper.
    run_case_1_two_detectors(passive_x)
    run_case_2_three_detectors(passive_x)
    run_case_3_intervention()
    run_case_4_stipulation(passive_x)

    # Case 5 uses its own generator (LEAK_RANDOM_SEED), so Cases 1-4 are
    # unchanged from version 1.0.2.
    run_case_5_leak()

    # Keep statistical label symmetry distinct from realiser permutation.
    report_label_swap_invariance(passive_x)


if __name__ == "__main__":
    main()