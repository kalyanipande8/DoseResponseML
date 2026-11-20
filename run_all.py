import json
import os

from src.simulate_dose_response import simulate, ENDPOINTS
from src.curve_fitting import fit_all_endpoints
from src.reporting import visual_predictive_check, parameter_summary_table


def main():
    records, true_params = simulate()
    fit_df = fit_all_endpoints(records, true_params)

    os.makedirs("output", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    visual_predictive_check(records, true_params, ENDPOINTS[0], "output/vpc_endpoint_00.png")
    parameter_summary_table(fit_df, "results/parameter_summary.csv", "results/parameter_summary.md")

    summary = {
        "n_pairs": len(records),
        "n_endpoints": len(ENDPOINTS),
        "mean_emax_r2": round(fit_df["emax_fit_r2"].mean(), 4),
        "mean_4pl_r2": round(fit_df["4pl_fit_r2"].mean(), 4),
        "mean_ec50_pct_error_emax": round(fit_df["emax_ec50_pct_error"].mean(), 2),
    }
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
