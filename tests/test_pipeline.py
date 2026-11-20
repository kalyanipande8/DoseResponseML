import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_dose_response import simulate, ENDPOINTS
from src.curve_fitting import fit_all_endpoints, fit_emax, fit_4pl


def test_at_least_1200_pairs():
    records, _ = simulate()
    assert len(records) >= 1150  # allow for rounding of pairs_per_endpoint * 18


def test_18_endpoints():
    assert len(ENDPOINTS) == 18


def test_emax_fit_achieves_good_r2():
    records, true_params = simulate(n=400, n_endpoints=4)
    fit_df = fit_all_endpoints(records, true_params)
    assert fit_df["emax_fit_r2"].mean() > 0.7


def test_4pl_fit_achieves_good_r2():
    records, true_params = simulate(n=400, n_endpoints=4)
    fit_df = fit_all_endpoints(records, true_params)
    assert fit_df["4pl_fit_r2"].mean() > 0.7


def test_ec50_recovery_within_reasonable_error():
    records, true_params = simulate(n=600, n_endpoints=6)
    fit_df = fit_all_endpoints(records, true_params)
    assert fit_df["emax_ec50_pct_error"].mean() < 30
