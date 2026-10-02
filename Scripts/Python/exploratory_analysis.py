import pandas as pd
import numpy as np

"""
So everything isn't printing and confusing what is being read, notes will have a #, while code will have ". 
"""

# Goal: Do some quick analysis on the data including but not limited to minimums, maximums, plotting, and totals. 

# Load files
freq = pd.read_csv(r"C:\SQL Data\freMTPL2freq.csv")
sev = pd.read_csv(r"C:\SQL Data\freMTPL2sev.csv")

# Quick file check
"""
print(freq.head())
print(sev.head())
print(freq.shape)
print(sev.shape)
"""

# Quick data validation comparison with SQL data.
"""
print(freq.isna().sum())
print(sev.isna().sum())
print(freq["Exposure"].describe())
print(freq["ClaimNb"].describe())
print(sev["ClaimAmount"].describe())
print(sev["ClaimAmount"].min())
print(sev["ClaimAmount"].max())
"""

# Portfolio Overall Claim Frequency
total_claims = freq["ClaimNb"].sum()
total_exposure = freq["Exposure"].sum()
overall_frequency = total_claims / total_exposure
"""
print("Total Claims:", total_claims)
print("Total Exposure:", total_exposure)
print("Overall Frequency:", overall_frequency)
"""

# Frequency by Driver Age
freq["DriverAgeBand"] = pd.cut(
    freq["DrivAge"],
    bins=[17, 24, 34, 44, 54, 64, 74, 100],
    labels=[
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65-74",
        "75+"
    ]
)
age_frequency = (
    freq.groupby("DriverAgeBand", observed=True).agg(
        Policies=("IDpol", "count"),
        Exposure=("Exposure", "sum"),
        Claims=("ClaimNb", "sum")
    ).reset_index()
)
age_frequency["Frequency"] = age_frequency["Claims"] / age_frequency["Exposure"]
"""
print(age_frequency)
"""

# Frequency by Bonus-Malus
freq["BonusMalusBand"] = pd.cut(
    freq["BonusMalus"],
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
bonus_frequency = (
    freq.groupby("BonusMalusBand", observed=True).agg(
        Policies=("IDpol", "count"),
        Exposure=("Exposure", "sum"),
        Claims=("ClaimNb", "sum")
    ).reset_index()
)
bonus_frequency["Frequency"] = bonus_frequency["Claims"] / bonus_frequency["Exposure"]
"""
print(bonus_frequency)
"""

freq["VehicleAgeBand"] = pd.cut(
    freq["VehAge"],
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
vehicle_age_frequency = (freq.groupby("VehicleAgeBand", observed=True).agg(
    Policies=("IDpol", "count"),
    Exposure=("Exposure", "sum"),
    Claims=("ClaimNb", "sum")
    ).reset_index()
)
vehicle_age_frequency["Frequency"] = vehicle_age_frequency["Claims"] / vehicle_age_frequency["Exposure"]
"""
print(vehicle_age_frequency)
"""
