"""Real nonlinear curve fitting of Emax and 4-parameter logistic (4PL,
sigmoidal) models via scipy.optimize.curve_fit, with fit-quality
comparison and recovery validation against the hidden true parameters."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from .simulate_dose_response import emax_model


def four_param_logistic(dose, bottom, top, ec50, hill):
    return bottom + (top - bottom) / (1 + (ec50 / np.maximum(dose, 1e-6)) ** hill)


def fit_emax(doses, responses):
    p0 = [responses.min(), responses.max() - responses.min(), np.median(doses), 1.0]
    try:
        popt, _ = curve_fit(emax_model, doses, responses, p0=p0, maxfev=8000,
                             bounds=([-50, 0, 0.01, 0.1], [200, 300, 500, 5]))
        pred = emax_model(doses, *popt)
        ss_res = np.sum((responses - pred) ** 2)
        ss_tot = np.sum((responses - responses.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        return {"e0": popt[0], "emax": popt[1], "ec50": popt[2], "hill": popt[3], "r2": r2}
    except Exception:
        return None


def fit_4pl(doses, responses):
    p0 = [responses.min(), responses.max(), np.median(doses), 1.0]
    try:
        popt, _ = curve_fit(four_param_logistic, doses, responses, p0=p0, maxfev=8000,
                             bounds=([-50, 0, 0.01, 0.1], [200, 300, 500, 10]))
        pred = four_param_logistic(doses, *popt)
        ss_res = np.sum((responses - pred) ** 2)
        ss_tot = np.sum((responses - responses.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        return {"bottom": popt[0], "top": popt[1], "ec50": popt[2], "hill": popt[3], "r2": r2}
    except Exception:
        return None


def fit_all_endpoints(records: list, true_params: dict) -> pd.DataFrame:
    df = pd.DataFrame(records)
    rows = []
    for ep, group in df.groupby("endpoint"):
        doses = group["dose"].values
        responses = group["response"].values
        emax_fit = fit_emax(doses, responses)
        pl4_fit = fit_4pl(doses, responses)
        true = true_params[ep]

        row = {"endpoint": ep, "true_ec50": true["ec50"], "true_emax": true["emax"]}
        if emax_fit:
            row["emax_fit_r2"] = round(emax_fit["r2"], 4)
            row["emax_ec50_est"] = round(emax_fit["ec50"], 4)
            row["emax_ec50_pct_error"] = round(100 * abs(emax_fit["ec50"] - true["ec50"]) / true["ec50"], 2)
        if pl4_fit:
            row["4pl_fit_r2"] = round(pl4_fit["r2"], 4)
            row["4pl_ec50_est"] = round(pl4_fit["ec50"], 4)
        rows.append(row)
    return pd.DataFrame(rows)
