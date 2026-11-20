# DoseResponseML

A dose-response modeling tool fitting Emax and 4-parameter logistic
(sigmoidal) curves across 18 endpoints, with visual predictive checks and
parameter summary reporting.

> Developed dose-response modeling tool evaluating 1,200+ exposure-efficacy
> pairs with Emax and sigmoidal fits.
> Built reporting module generating visual predictive checks and parameter
> summary tables for 18 endpoints.

## What's real vs. synthetic — read this first

**Real:** `src/curve_fitting.py` performs genuine nonlinear curve fitting
(`scipy.optimize.curve_fit`) of both the Emax model and the 4-parameter
logistic (4PL/sigmoidal) model to each endpoint's dose-response data, with
real R-squared fit-quality metrics and EC50-recovery error computed against
the hidden true parameters. `src/reporting.py` generates a real visual
predictive check plot (observed data vs. the true underlying curve) and a
real parameter summary table (CSV + Markdown). R is not available in this
execution environment, so `docs/drc_reference.R` is an
authored-but-not-executed reference showing the equivalent fit using R's
`drc` package — every number below comes from the executed Python mirror.

**Synthetic:** there is no real clinical exposure-efficacy dataset in this
environment. `src/simulate_dose_response.py` generates 1,206 exposure-
efficacy pairs across 18 endpoints, each with a hidden true Emax/EC50/Hill
relationship and independent measurement noise, set before any fitting code
runs.

## Results (real, from `run_all.py`)

```
1,206 exposure-efficacy pairs, 18 endpoints

Emax model:  mean R^2 = 0.9091, mean EC50 % error = 10.17%
4PL model:   mean R^2 = 0.9091
```

Both models achieve strong fit quality (R^2 ~0.91) and the Emax model
recovers EC50 within 10.17% average error across the 18 endpoints,
despite ~6% proportional measurement noise added independently of the
fitting code — a real, honest validation of the curve-fitting pipeline's
ability to recover ground truth under realistic noise.

`tests/test_pipeline.py` (5 tests, all passing) checks pair count >=1150
(allowing for integer-division rounding across 18 endpoints), endpoint
count ==18, both models achieve R^2 > 0.7 on a smaller validation set, and
EC50 recovery error stays under 30%.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_dose_response.py   # 1,206-pair, 18-endpoint simulation with true Emax/EC50
  curve_fitting.py              # Emax + 4PL nonlinear curve fitting (scipy.optimize.curve_fit)
  reporting.py                    # visual predictive check plots + parameter summary tables
docs/
  drc_reference.R                  # authored-but-unexecuted R reference (drc package)
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, scipy, numpy, pandas, matplotlib, pytest. R reference
documented but not executed.

## Limitations

- No real clinical exposure-efficacy dataset is used; all pairs are
  simulated.
- EC50 recovery error (10.17% average) varies by endpoint depending on
  how well the sampled dose range straddles the true EC50 — some endpoints
  show higher error when doses are sparse near the inflection point,
  a realistic experimental-design limitation rather than a fitting bug.
