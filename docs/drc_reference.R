# Authored-but-not-executed R reference.
# This project was built and validated in Python (see src/) because R is
# not available in this execution environment. This file documents how the
# same dose-response modeling would be done in R using the standard drc
# package, for reference/portability.

library(drc)
library(dplyr)

data <- read.csv("simulated_dose_response.csv")  # columns: endpoint, dose, response

fit_one_endpoint <- function(sub_data) {
  # 4-parameter log-logistic (equivalent to the 4PL sigmoidal model)
  model_4pl <- drm(response ~ dose, data = sub_data, fct = LL.4())

  # Emax model (drc's own Emax parameterization)
  model_emax <- drm(response ~ dose, data = sub_data, fct = EXD.3())

  list(
    fourpl_ec50 = coef(model_4pl)["ED50:(Intercept)"],
    fourpl_r2 = 1 - sum(residuals(model_4pl)^2) / sum((sub_data$response - mean(sub_data$response))^2),
    emax_ec50 = coef(model_emax)["ED50:(Intercept)"]
  )
}

results <- data %>%
  group_by(endpoint) %>%
  group_modify(~ as.data.frame(fit_one_endpoint(.x)))

write.csv(results, "parameter_summary.csv", row.names = FALSE)

# Visual predictive check for one endpoint
plot(model_4pl <- drm(response ~ dose, data = filter(data, endpoint == "endpoint_00"), fct = LL.4()),
     main = "VPC: endpoint_00")
