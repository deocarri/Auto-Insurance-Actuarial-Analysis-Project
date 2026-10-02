import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split

freq = pd.read_csv(r"C:\SQL Data\freMTPL2freq.csv")
sev = pd.read_csv(r"C:\SQL Data\freMTPL2sev.csv")

"""
So everything isn't printing and confusing what is being read, notes will have a #, while code will have ". 
"""

# Goal: Predict claim frequency using policyholder and vehicle characteristics.

# Split the frequency data using an 80/20 train/test split.
train_freq, test_freq = train_test_split(
    freq,
    test_size=0.20,
    random_state=42
)

# Fit a Poisson model.
frequency_model = smf.glm(
    formula="""
        ClaimNb ~
        DrivAge + 
        VehAge + 
        VehPower + 
        BonusMalus + 
        C(VehBrand) + 
        C(VehGas) + 
        C(Area) + 
        C(Region)
    """,
    data=train_freq,
    family=sm.families.Poisson(),
    offset=np.log(train_freq["Exposure"])
).fit()
"""
print(frequency_model.summary())
"""

# Check for Pearson dispersion for overdispersion. An overdispersion greatly more than 1 indicates overdispersion.
dispersion = frequency_model.pearson_chi2 / frequency_model.df_resid
"""
print("Dispersion:", dispersion)
"""
# The dispersion of 2.62 indicates high overdispersion and Poisson should be avoided from being used.

# Fit a negative binomial model.
frequency_nb_model = smf.glm(
    formula="""
        ClaimNb ~
        DrivAge + 
        VehAge + 
        VehPower + 
        BonusMalus + 
        C(VehBrand) + 
        C(VehGas) + 
        C(Area) + 
        C(Region)
    """,
    data=train_freq,
    family=sm.families.NegativeBinomial(),
    offset=np.log(train_freq["Exposure"])
).fit()
"""
print(frequency_nb_model.summary())
"""

# Compare models using Akaike Information Criterion (AIC). A lower AIC indicates a better fit among the models being
# compared. However, do not use solely this to choose a model, it only helps affirm what you know.
"""
print("Poisson AIC:", frequency_model.aic)
print("Negative Binomial AIC:", frequency_nb_model.aic)
"""
# With Negative Binomial lower then Poisson and high overdispersion, we will move forward with negative binomial.

# Generate frequency predictions
test_freq["PredictedClaims"] = frequency_nb_model.predict(
    test_freq,
    offset=np.log(test_freq["Exposure"])
)
test_freq["PredictedFrequency"] = test_freq["PredictedClaims"] / test_freq["Exposure"]

# Create a copy to download as a CSV file.
frequency_validation = test_freq[
    ["IDpol", "Exposure", "ClaimNb", "PredictedClaims", "PredictedFrequency"]
].copy()

frequency_validation.to_csv(r"C:\SQL Data\Auto Insurance Actuarial\frequency_validation.csv", index=False)
