import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from frequency_analysis import test_freq

freq = pd.read_csv(r"C:\SQL Data\freMTPL2freq.csv")
sev = pd.read_csv(r"C:\SQL Data\freMTPL2sev.csv")

"""
So everything isn't printing and confusing what is being read, notes will have a #, while code will have ". 
"""

# Goal: Build the severity model using a Gamma GLM with a log link.

# Severity model preparation
train_sev, test_sev = train_test_split(
    sev,
    test_size=0.20,
    random_state=42
)

# Join frequency and severity datasets
train_sev_model = train_sev.merge(
    freq,
    on="IDpol",
    how="inner"
)
test_sev_model = test_sev.merge(
    freq,
    on="IDpol",
    how="inner"
)

# Fit the gamma severity GLM
severity_model = smf.glm(
    formula="""
        ClaimAmount ~ 
        DrivAge +
        VehAge + 
        VehPower + 
        BonusMalus + 
        C(VehBrand) + 
        C(VehGas) + 
        C(Area) + 
        C(Region)
    """,
    data=train_sev_model,
    family=sm.families.Gamma(
        link=sm.families.links.Log()
    )
).fit()
"""
print(severity_model.summary())
"""

# Generate severity predictions
test_sev_model["PredictedSeverity"] = severity_model.predict(test_sev_model)

# Save the predictions as a CSV file for future use.
severity_validation = test_sev_model[
    ["IDpol", "ClaimAmount", "PredictedSeverity"]
].copy()
severity_validation.to_csv(r"C:\SQL Data\Auto Insurance Actuarial\severity_validation.csv", index=False)

# Now that we have predicted severity and predicted frequency, we can calculate expected loss cost.
validation = test_freq.copy()
validation["PredictedSeverity"] = severity_model.predict(validation)
validation["PredictedLossCost"] = validation["PredictedFrequency"] * validation["PredictedSeverity"]
# With this, every policy has IDpol, Exposure, ClaimNb, PredictedClaims, PredictedFrequency, PredictedSeverity,
# and PredictedLossCost.

# Now we bring in the observed Loss Cost for comparison, however we still have to be careful due to the
# severity data not perfectly reconciling with the frequency data.
observed_severity_by_policy = (sev.groupby("IDpol").agg(
    ObservedClaimAmount=("ClaimAmount", "sum"),
    SeverityClaimCount=("ClaimAmount", "count")
    ).reset_index()
)
validation = validation.merge(
    observed_severity_by_policy,
    on="IDpol",
    how="left"
)

# Create a flag for missing values.
validation["HasSeverityRecord"] = validation["SeverityClaimCount"].notna()
# Do not replace missing values for 0. Just because it is missing, doesn't mean it is 0.

# For matching policies.
matched_validation = validation[
    validation["HasSeverityRecord"]
].copy()

# Observed Loss Cost calculation.
matched_validation["ObservedLossCost"] = matched_validation["ObservedClaimAmount"] / matched_validation["Exposure"]
