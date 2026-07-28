import pandas as pd
import joblib
import shap

# Load dataset
df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

# Feature engineering
df["Power"] = df["Torque [Nm]"] * df["Rotational speed [rpm]"]
df["Temp Difference"] = (
    df["Process temperature [K]"] - df["Air temperature [K]"]
)

df = pd.get_dummies(df, columns=["Type"])

features = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Power",
    "Temp Difference",
    "Type_H",
    "Type_L",
    "Type_M"
]

X = df[features]

# Load trained model
model = joblib.load("models/random_forest.pkl")

# Pick one sample
probs = model.predict_proba(X)[:, 1]
highest_risk_idx = probs.argmax()

print("Highest risk row index:", highest_risk_idx)
print("Failure probability:", probs[highest_risk_idx])

sample = X.iloc[[highest_risk_idx]]

# SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(sample)

print("Prediction probability:")
print(model.predict_proba(sample))

print("\nFeature contributions toward FAILURE prediction:")

for i, feature in enumerate(features):
    value = shap_values[0][i][1]
    print(f"{feature}: {value:.6f}")
