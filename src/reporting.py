"""Real reporting module: visual predictive checks (VPC) and parameter
summary tables."""
from __future__ import annotations

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .simulate_dose_response import emax_model


def visual_predictive_check(records: list, true_params: dict, endpoint: str, out_path: str):
    df = pd.DataFrame(records)
    sub = df[df["endpoint"] == endpoint]
    doses = sub["dose"].values
    responses = sub["response"].values
    p = true_params[endpoint]

    dose_grid = np.linspace(doses.min(), doses.max(), 200)
    true_curve = emax_model(dose_grid, p["e0"], p["emax"], p["ec50"], p["hill"])

    fig, ax = plt.subplots()
    ax.scatter(doses, responses, alpha=0.4, s=15, label="observed")
    ax.plot(dose_grid, true_curve, color="red", label="true Emax curve")
    ax.set_xlabel("Dose")
    ax.set_ylabel("Response")
    ax.set_title(f"Visual predictive check: {endpoint}")
    ax.legend()
    fig.savefig(out_path, dpi=80)
    plt.close(fig)


def parameter_summary_table(fit_results: pd.DataFrame, out_csv: str, out_md: str):
    fit_results.to_csv(out_csv, index=False)
    with open(out_md, "w") as f:
        f.write(fit_results.to_markdown(index=False))
