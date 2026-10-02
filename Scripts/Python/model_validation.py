import pandas as pd
import numpy as np
from frequency_analysis import test_freq
from severity_model import test_sev_model
from severity_model import matched_validation
from severity_model import validation

freq = pd.read_csv(r"C:\SQL Data\freMTPL2freq.csv")
sev = pd.read_csv(r"C:\SQL Data\freMTPL2sev.csv")

# Goal: Run checks on the models and compare with the observed data to validate if the models are viable.

# Frequency validation
# Overall Observed Frequency
observed_frequency = test_freq["ClaimNb"].sum() / test_freq["Exposure"].sum()

# Predicted Frequency
predicted_frequency = test_freq["PredictedClaims"].sum() / test_freq["Exposure"].sum()

# Error between observed and predicted
frequency_error = predicted_frequency - observed_frequency
frequency_percent_error = frequency_error / observed_frequency

# Frequency validation by Driver Age
test_freq["DriverAgeBand"] = pd.cut(
    test_freq["DrivAge"],
    bins=[17, 24, 34, 44, 54, 64, 74, 100],
    labels=[
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65-74",
        "75+"]
)
frequency_validation_by_driver_age = (
    test_freq.groupby("DriverAgeBand", observed=True).agg(
        Policies=("IDpol", "count"),
        Exposure=("Exposure", "sum"),
        ObservedClaims=("ClaimNb", "sum"),
        PredictedClaims=("PredictedClaims", "sum")
    ).reset_index()
)
frequency_validation_by_driver_age["ObservedFrequency"] = (frequency_validation_by_driver_age["ObservedClaims"] /
                                                           frequency_validation_by_driver_age["Exposure"])
frequency_validation_by_driver_age["PredictedFrequency"] = (frequency_validation_by_driver_age["PredictedClaims"] /
                                                            frequency_validation_by_driver_age["Exposure"])
frequency_validation_by_driver_age["Difference"] = (frequency_validation_by_driver_age["PredictedFrequency"] -
                                                    frequency_validation_by_driver_age["ObservedFrequency"])
frequency_validation_by_driver_age["PercentError"] = (frequency_validation_by_driver_age["Difference"] /
                                                      frequency_validation_by_driver_age["ObservedFrequency"])

# Do the same validation for Bonus-Malus, Vehicle Age, Area, Region
# Bonus-Malus validation
test_freq["BonusMalusBand"] = pd.cut(
    test_freq["BonusMalus"],
    bins=[0, 79, 99, 119, 139, 159, np.inf],
    labels=[
        "<80",
        "80-99",
        "100-119",
        "120-139",
        "140-159",
        "160+"
    ]
)
frequency_validation_by_bonus_malus = (
    test_freq.groupby("BonusMalusBand", observed=True).agg(
        Policies=("IDpol", "count"),
        Exposure=("Exposure", "sum"),
        ObservedClaims=("ClaimNb", "sum"),
        PredictedClaims=("PredictedClaims", "sum")
    ).reset_index()
)
frequency_validation_by_bonus_malus["ObservedFrequency"] = (frequency_validation_by_bonus_malus["ObservedClaims"] /
                                                            frequency_validation_by_bonus_malus["Exposure"])
frequency_validation_by_bonus_malus["PredictedFrequency"] = (frequency_validation_by_bonus_malus["PredictedClaims"] /
                                                             frequency_validation_by_bonus_malus["Exposure"])
frequency_validation_by_bonus_malus["Difference"] = (frequency_validation_by_bonus_malus["PredictedFrequency"] -
                                                     frequency_validation_by_bonus_malus["ObservedFrequency"])
frequency_validation_by_bonus_malus["PercentError"] = (frequency_validation_by_bonus_malus["Difference"] /
                                                       frequency_validation_by_bonus_malus["ObservedFrequency"])

# Vehicle Age validation
test_freq["VehicleAgeBand"] = pd.cut(
    test_freq["VehAge"],
    bins=[-1, 4, 9, 14, 19, 29, np.inf],
    labels=[
        "0-4",
        "5-9",
        "10-14",
        "15-19",
        "20-29",
        "30+"
    ]
)
frequency_validation_by_vehicle_age = (test_freq.groupby("VehicleAgeBand", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    ObservedClaims=("ClaimNb", "sum"),
    PredictedClaims=("PredictedClaims", "sum")
    ).reset_index()
)
frequency_validation_by_vehicle_age["ObservedFrequency"] = (frequency_validation_by_vehicle_age["ObservedClaims"] /
                                                            frequency_validation_by_vehicle_age["Exposure"])
frequency_validation_by_vehicle_age["PredictedFrequency"] = (frequency_validation_by_vehicle_age["PredictedClaims"] /
                                                             frequency_validation_by_vehicle_age["Exposure"])
frequency_validation_by_vehicle_age["Difference"] = (frequency_validation_by_vehicle_age["PredictedFrequency"] -
                                                     frequency_validation_by_vehicle_age["ObservedFrequency"])
frequency_validation_by_vehicle_age["PercentError"] = (frequency_validation_by_vehicle_age["Difference"] /
                                                       frequency_validation_by_vehicle_age["ObservedFrequency"])

# Area validation
frequency_validation_by_area = (test_freq.groupby("Area", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    ObservedClaims=("ClaimNb", "sum"),
    PredictedClaims=("PredictedClaims", "sum")
    ).reset_index()
)
frequency_validation_by_area["ObservedFrequency"] = (frequency_validation_by_area["ObservedClaims"] /
                                                     frequency_validation_by_area["Exposure"])
frequency_validation_by_area["PredictedFrequency"] = (frequency_validation_by_area["PredictedClaims"] /
                                                      frequency_validation_by_area["Exposure"])
frequency_validation_by_area["Difference"] = (frequency_validation_by_area["PredictedFrequency"] -
                                              frequency_validation_by_area["ObservedFrequency"])
frequency_validation_by_area["PercentError"] = (frequency_validation_by_area["Difference"] /
                                                frequency_validation_by_area["ObservedFrequency"])

# Region validation
frequency_validation_by_region = (test_freq.groupby("Region", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    ObservedClaims=("ClaimNb", "sum"),
    PredictedClaims=("PredictedClaims", "sum")
    ).reset_index()
)
frequency_validation_by_region["ObservedFrequency"] = (frequency_validation_by_region["ObservedClaims"] /
                                                       frequency_validation_by_region["Exposure"])
frequency_validation_by_region["PredictedFrequency"] = (frequency_validation_by_region["PredictedClaims"] /
                                                        frequency_validation_by_region["Exposure"])
frequency_validation_by_region["Difference"] = (frequency_validation_by_region["PredictedFrequency"] -
                                                frequency_validation_by_region["ObservedFrequency"])
frequency_validation_by_region["PercentError"] = (frequency_validation_by_region["Difference"] /
                                                  frequency_validation_by_region["ObservedFrequency"])


# Severity validation:
# Start with some Observed and Predicted statistics as a dataframe.
severity_validation_summary = pd.DataFrame({
    "Metric": [
        "Number of Test Claims",
        "Observed Mean Severity",
        "Predicted Mean Severity",
        "Observed Median Severity",
        "Observed 90th Percentile",
        "Observed 99th Percentile",
        "Observed 99.9th Percentile"
    ],
    "Value": [
        len(test_sev_model),
        test_sev_model["ClaimAmount"].mean(),
        test_sev_model["PredictedSeverity"].mean(),
        test_sev_model["ClaimAmount"].median(),
        test_sev_model["ClaimAmount"].quantile(0.90),
        test_sev_model["ClaimAmount"].quantile(0.95),
        test_sev_model["ClaimAmount"].quantile(0.99)
    ]
})

# Severity comparison based on quantile range with observed and predicted amounts
quantile_levels = [0.5, 0.75, 0.9, 0.95, 0.99, 0.999]
severity_quantile_validation = pd.DataFrame({
    "Quantile": quantile_levels,
    "Observed": [
        test_sev_model["ClaimAmount"].quantile(q)
        for q in quantile_levels
    ],
    "Predicted": [
        test_sev_model["PredictedSeverity"].quantile(q)
        for q in quantile_levels
    ]
})
severity_quantile_validation["Difference"] = (severity_quantile_validation["Predicted"] -
                                              severity_quantile_validation["Observed"])


# Loss Cost validation using the matched severity data due to the mismatch in severity and frequency data.
# The bands have to be added into the matched validation dataframe.
matched_validation["DriverAgeBand"] = pd.cut(
    matched_validation["DrivAge"],
    bins=[17, 24, 34, 44, 54, 64, 74, 100],
    labels=[
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65-74",
        "75+"]
)
loss_validation_by_driver_age = (matched_validation.groupby("DriverAgeBand", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    ObservedLoss=("ObservedClaimAmount", "sum"),
    PredictedLoss=("PredictedLossCost", "sum")
).reset_index())
loss_validation_by_driver_age["ObservedLossCost"] = (loss_validation_by_driver_age["ObservedLoss"] /
                                                     loss_validation_by_driver_age["Exposure"])
loss_validation_by_driver_age["PredictedLossCost"] = (loss_validation_by_driver_age["PredictedLoss"] /
                                                      loss_validation_by_driver_age["Exposure"])
loss_validation_by_driver_age["Difference"] = (loss_validation_by_driver_age["PredictedLossCost"] -
                                               loss_validation_by_driver_age["ObservedLossCost"])
loss_validation_by_driver_age["PercentError"] = (loss_validation_by_driver_age["Difference"] /
                                                 loss_validation_by_driver_age["ObservedLossCost"])

# Repeat this Loss Cost validation for Bonus-Malus, Vehicle Age, Area, Region
# Bonus-Malus Loss Cost validation
matched_validation["BonusMalusBand"] = pd.cut(
    matched_validation["BonusMalus"],
    bins=[0, 79, 99, 119, 139, 159, np.inf],
    labels=[
        "<80",
        "80-99",
        "100-119",
        "120-139",
        "140-159",
        "160+"
    ]
)
loss_validation_by_bonus_malus = (matched_validation.groupby("DriverAgeBand", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    ObservedLoss=("ObservedClaimAmount", "sum"),
    PredictedLoss=("PredictedLossCost", "sum")
).reset_index())
loss_validation_by_bonus_malus["ObservedLossCost"] = (loss_validation_by_bonus_malus["ObservedLoss"] /
                                                      loss_validation_by_bonus_malus["Exposure"])
loss_validation_by_bonus_malus["PredictedLossCost"] = (loss_validation_by_bonus_malus["PredictedLoss"] /
                                                       loss_validation_by_bonus_malus["Exposure"])
loss_validation_by_bonus_malus["Difference"] = (loss_validation_by_bonus_malus["PredictedLossCost"] -
                                                loss_validation_by_bonus_malus["ObservedLossCost"])
loss_validation_by_bonus_malus["PercentError"] = (loss_validation_by_bonus_malus["Difference"] /
                                                  loss_validation_by_bonus_malus["ObservedLossCost"])

# Loss Cost by Vehicle Age
matched_validation["VehicleAgeBand"] = pd.cut(
    matched_validation["VehAge"],
    bins=[-1, 4, 9, 14, 19, 29, np.inf],
    labels=[
        "0-4",
        "5-9",
        "10-14",
        "15-19",
        "20-29",
        "30+"
    ]
)
loss_validation_by_vehicle_age = (matched_validation.groupby("DriverAgeBand", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    ObservedLoss=("ObservedClaimAmount", "sum"),
    PredictedLoss=("PredictedLossCost", "sum")
).reset_index())
loss_validation_by_vehicle_age["ObservedLossCost"] = (loss_validation_by_vehicle_age["ObservedLoss"] /
                                                      loss_validation_by_vehicle_age["Exposure"])
loss_validation_by_vehicle_age["PredictedLossCost"] = (loss_validation_by_vehicle_age["PredictedLoss"] /
                                                       loss_validation_by_vehicle_age["Exposure"])
loss_validation_by_vehicle_age["Difference"] = (loss_validation_by_vehicle_age["PredictedLossCost"] -
                                                loss_validation_by_vehicle_age["ObservedLossCost"])
loss_validation_by_vehicle_age["PercentError"] = (loss_validation_by_vehicle_age["Difference"] /
                                                  loss_validation_by_vehicle_age["ObservedLossCost"])

# Loss Cost by Area
loss_cost_validation_by_area = (matched_validation.groupby("Area", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    ObservedClaims=("ClaimNb", "sum"),
    PredictedClaims=("PredictedClaims", "sum")
    ).reset_index()
)
loss_cost_validation_by_area["ObservedFrequency"] = (loss_cost_validation_by_area["ObservedClaims"] /
                                                     loss_cost_validation_by_area["Exposure"])
loss_cost_validation_by_area["PredictedFrequency"] = (loss_cost_validation_by_area["PredictedClaims"] /
                                                      loss_cost_validation_by_area["Exposure"])
loss_cost_validation_by_area["Difference"] = (loss_cost_validation_by_area["PredictedFrequency"] -
                                              loss_cost_validation_by_area["ObservedFrequency"])
loss_cost_validation_by_area["PercentError"] = (loss_cost_validation_by_area["Difference"] /
                                                loss_cost_validation_by_area["ObservedFrequency"])

# Loss Cost by Region
loss_cost_validation_by_region = (matched_validation.groupby("Region", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    ObservedClaims=("ClaimNb", "sum"),
    PredictedClaims=("PredictedClaims", "sum")
    ).reset_index()
)
loss_cost_validation_by_region["ObservedFrequency"] = (loss_cost_validation_by_region["ObservedClaims"] /
                                                       loss_cost_validation_by_region["Exposure"])
loss_cost_validation_by_region["PredictedFrequency"] = (loss_cost_validation_by_region["PredictedClaims"] /
                                                        loss_cost_validation_by_region["Exposure"])
loss_cost_validation_by_region["Difference"] = (loss_cost_validation_by_region["PredictedFrequency"] -
                                                loss_cost_validation_by_region["ObservedFrequency"])
loss_cost_validation_by_region["PercentError"] = (loss_cost_validation_by_region["Difference"] /
                                                  loss_cost_validation_by_region["ObservedFrequency"])

# Download important files as CSV for future use.
validation.to_csv(r"C:\SQL Data\Auto Insurance Actuarial\policy_level_validation.csv", index=False)

severity_quantile_validation.to_csv(r"C:\SQL Data\Auto Insurance Actuarial\severity_quantile_validation.csv",
                                    index=False)

loss_validation_by_driver_age.to_csv(r"C:\SQL Data\Auto Insurance Actuarial\LossCost_Validation_By_Driver_Age.csv",
                                     index=False)

frequency_validation_by_driver_age.\
    to_csv(r"C:\SQL Data\Auto Insurance Actuarial\frequency_validation_by_driver_age.csv", index=False)
