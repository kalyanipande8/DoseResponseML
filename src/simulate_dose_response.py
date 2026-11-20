"""Simulate 1,200+ exposure-efficacy pairs across 18 endpoints with a
hidden true Emax/EC50 relationship, independent of the fitting code."""
from __future__ import annotations

import numpy as np

N_PAIRS = 1220
N_ENDPOINTS = 18
SEED = 808


def emax_model(dose, e0, emax, ec50, hill=1.0):
    return e0 + (emax * dose ** hill) / (ec50 ** hill + dose ** hill)


def simulate(n: int = N_PAIRS, n_endpoints: int = N_ENDPOINTS, seed: int = SEED):
    rng = np.random.default_rng(seed)
    endpoints = [f"endpoint_{i:02d}" for i in range(n_endpoints)]

    # true parameters per endpoint, independent of fitting code
    true_params = {}
    for ep in endpoints:
        true_params[ep] = {
            "e0": rng.uniform(0, 10),
            "emax": rng.uniform(40, 100),
            "ec50": rng.uniform(5, 50),
            "hill": rng.uniform(0.8, 2.5),
        }

    pairs_per_endpoint = n // n_endpoints
    records = []
    for ep in endpoints:
        p = true_params[ep]
        doses = rng.uniform(0.1, 150, pairs_per_endpoint)
        true_response = emax_model(doses, p["e0"], p["emax"], p["ec50"], p["hill"])
        noise = rng.normal(0, 0.06 * (p["emax"] + p["e0"]), pairs_per_endpoint)
        observed = true_response + noise
        for d, r in zip(doses, observed):
            records.append({"endpoint": ep, "dose": d, "response": r})

    return records, true_params


ENDPOINTS = [f"endpoint_{i:02d}" for i in range(N_ENDPOINTS)]
assert len(ENDPOINTS) == 18
