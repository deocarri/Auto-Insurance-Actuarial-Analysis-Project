import pandas as pd
import numpy as np
import scipy.stats as stats

freq = pd.read_csv(r"C:\SQL Data\freMTPL2freq.csv")
sev = pd.read_csv(r"C:\SQL Data\freMTPL2sev.csv")

"""
So everything isn't printing and confusing what is being read, notes will have a #, while code will have ". 
"""

# Goal: Examine the severity distribution

# Quick severity analysis
quantiles = [0.5, 0.75, 0.9, 0.95, 0.99, 0.999]
"""
print("Severity Median:", sev["ClaimAmount"].median())
print("Severity Mean:", sev["ClaimAmount"].mean())
print("Severity Max:", sev["ClaimAmount"].max())
severity_quantiles = sev["ClaimAmount"].quantile(quantiles)
print(severity_quantiles)
"""

# Calculate expected shortfall for severity tail analysis.
var_99 = sev["ClaimAmount"].quantile(0.99)
expected_shortfall_99 = (sev.loc[sev["ClaimAmount"] >= var_99, "ClaimAmount"].mean())
"""
print("99% VaR:", var_99)
print("99% Expected Shortfall:", expected_shortfall_99)
"""

# You can clearly see a heavy right-skew due to a huge difference in mean and median.
# Create a plot showing the severity distribution.
"""
plt.figure(figsize=(10, 6))
plt.hist(
    sev["ClaimAmount"],
    bins=100
)
plt.xlabel("Claim Amount")
plt.ylabel("Number of Claims")
plt.title("Auto Insurance Claim Severity")
plt.show()
"""

# Due to the extremely heavy right-skew, I will make a log severity.
"""
sev["LogClaimAmount"] = np.log(sev["ClaimAmount"])
plt.figure(figsize=(10, 6))
plt.hist(
    sev["LogClaimAmount"],
    bins=100
)
plt.xlabel("Log Claim Amount")
plt.ylabel("Number of Claims")
plt.title("Log Claim Severity Distribution")
plt.show()
"""

# Knowing that the log severity fit better, I will compare other possibilities: lognormal, gamma, and pareto.
claims = sev["ClaimAmount"].values

lognorm_params = stats.lognorm.fit(claims, floc=0)
gamma_params = stats.gamma.fit(claims, floc=0)
pareto_params = stats.pareto.fit(claims, floc=0)

# Define AIC and BIC(Bayesian Information Criterion) calculation
def calculate_aic_bic(log_likelihood, num_params, n):
    aic = 2 * num_params - 2 * log_likelihood
    bic = num_params * np.log(n) - 2 * log_likelihood
    return aic, bic


# Calculate log likelihoods.
lognorm_ll = np.sum(
    stats.lognorm.logpdf(
        claims,
        *lognorm_params
    )
)
gamma_ll = np.sum(
    stats.gamma.logpdf(
        claims,
        *gamma_params
    )
)
pareto_ll = np.sum(
    stats.pareto.logpdf(
        claims,
        *pareto_params
    )
)
ks_lognorm = stats.kstest(
    claims,
    "lognorm",
    args=lognorm_params
)
ks_gamma = stats.kstest(
    claims,
    "gamma",
    args=gamma_params
)
ks_pareto = stats.kstest(
    claims,
    "pareto",
    args=pareto_params
)

# Use the AIC, BIC, and KS calculations to make a decision on which one to use.
n = len(claims)

print("Lognorm Likelihood AIC/BIC/KS:", calculate_aic_bic(lognorm_ll, 2, n), ks_lognorm.statistic)
print("Gamma Likelihood AIC/BIC/KS:", calculate_aic_bic(gamma_ll, 2, n), ks_gamma.statistic)
print("Pareto Likelihood AIC/BIC/KS:", calculate_aic_bic(pareto_ll, 2, n), ks_pareto.statistic)

# Due to the values being strictly positive, extremely right-skewed, and continuous, I will be building the
# severity model with a Gamma GLM with a log link.
