#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
three_detector.py
=================

Version:
    1.0.1 (2026-09-28)

Supplementary research code for:

    Peter Kahl, "What Conceptual Change Cannot Recover:
    Interface Closure and Representational Sealing" (2026),
    §10, "A toy model of sealing: three detectors".

Author:
    Peter Kahl
    Independent researcher, Lex et Ratio
    https://www.lexetratio.com
    ORCID: 0009-0003-1616-4843

Repository:
    GitHub: https://github.com/Peter-Kahl/interface-closure-representational-sealing

Archive:
    Zenodo: https://doi.org/10.5281/zenodo.XXXXXXXX

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
paper. It simulates a binary latent target state G in {a, b} observed through
conditionally independent noisy binary detectors. It then fits latent-class
models by expectation-maximisation (EM) from multiple random initialisations.

The script illustrates four claims made in §10:

    1. With only two detectors, the role-level statistical structure is
       ordinarily non-identifiable: multiple distinct near-optimal parameter
       solutions can fit the same observed distribution.

    2. With three suitable conditionally independent detectors, the role-level
       structure is generically identifiable up to permutation of the two
       latent-state labels.

    3. Adding an intervention whose influence is mediated entirely through the
       same role-level state enriches the observational regime but does not, by
       itself, attach an independently specified realiser kind to either
       latent state or break a permutation of role-exceeding realisers.

    4. Fixing P(X1=1 | G=a)=0.9 breaks the statistical label symmetry by
       stipulation. It fixes which latent position is called 'a'; it does not
       establish which role-exceeding realiser occupies that position.

Interface interpretation
------------------------
The paper distinguishes the causal interface from the statistical factor it
induces. In this toy model, every detector and intervention accessible to the
simulated layer is mediated by the role-level latent state G:

    role-exceeding realiser / property Q
                    |
                    v
             role-level state G
              /      |      \
             v       v       v
            X1      X2      X3

and, in the intervention case:

             U ---> G ---> (X1, X2, X3)

There is no direct Q -> Xi measurement path.

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

    * intervention through G does not test whether some different intervention
      or measurement could breach the stipulated interface; and

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

Because all cases share one pseudo-random generator, changing the order or
number of random draws in an earlier case can change the generated data or EM
initialisations in later cases even when RANDOM_SEED is unchanged. Exact
reproduction therefore requires the same script version as well as the same
seed and compatible software environment.

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

SCRIPT_VERSION = "1.0.1"

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
TRUE_P = np.array([0.90, 0.80, 0.85], dtype=float)  # P(Xj=1 | G=a)
TRUE_Q = np.array([0.20, 0.10, 0.30], dtype=float)  # P(Xj=1 | G=b)

# Intervention parameters: P(G=a | U=0), P(G=a | U=1).
TRUE_R = np.array([0.20, 0.80], dtype=float)


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

    # True denotes the role-level state G=a.
    g_is_a = rng.random(n) < prob_a

    x = np.empty((n, len(p)), dtype=int)

    for j in range(len(p)):
        draw_if_a = rng.random(n) < p[j]
        draw_if_b = rng.random(n) < q[j]
        x[:, j] = np.where(g_is_a, draw_if_a, draw_if_b)

    return x


def loglik_and_posterior(
    x: np.ndarray,
    prob_a: float | np.ndarray,
    p: np.ndarray,
    q: np.ndarray,
) -> tuple[float, np.ndarray]:
    """Compute observed-data log-likelihood and posterior P(G=a | record)."""
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
    print(f"P(G=a) = {TRUE_PI}")
    print(f"P(Xj=1 | G=a) = {format_vector(TRUE_P, 2)}")
    print(f"P(Xj=1 | G=b) = {format_vector(TRUE_Q, 2)}")
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
    Case 3: add a randomised intervention U whose effect is mediated by G.

    U changes P(G=a) across intervention conditions, enriching the role-level
    observational structure. Because U reaches the detectors only through G,
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
        "Case 3. three detectors + role-mediated intervention",
        fits,
    )

    print(
        "The intervention changes the role-level prior but remains mediated "
        "through G; it supplies no direct Q-sensitive observation and "
        "therefore does not break realiser permutation behind the stipulated "
        "interface."
    )


def run_case_4_stipulation(
    x_three: np.ndarray,
) -> None:
    """
    Case 4: stipulate P(X1=1 | G=a)=0.9.

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
        "Case 4. conventional stipulation P(X1=1 | G=a)=0.9",
        fits,
    )

    print(
        "The stipulation fixes a statistical orientation only; it is not a "
        "target-side anchor and does not add a new measurement path."
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
    the intervention U.

    All random draws use the same seeded NumPy generator. Consequently, the
    exact Case 3 data and later EM initialisations depend on the sequence of
    random draws made by earlier cases. Exact numerical reproduction therefore
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

    # Keep statistical label symmetry distinct from realiser permutation.
    report_label_swap_invariance(passive_x)


if __name__ == "__main__":
    main()