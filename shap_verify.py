import pandas as pd
import joblib
import shap
import numpy as np

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

# ----------------------------
# Feature Engineering
# ----------------------------
df["Power"] = (
    df["Torque [Nm]"] *
    df["Rotational speed [rpm]"]
)

df["Temp Difference"] = (
    df["Process temperature [K]"] -
    df["Air temperature [K]"]
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

# ----------------------------
# Load trained model
# ----------------------------
model = joblib.load("models/random_forest.pkl")

# ----------------------------
# Highest-risk sample
# ----------------------------
probs = model.predict_proba(X)[:, 1]
idx = probs.argmax()

sample = X.iloc[[idx]]

print(f"\nHighest Risk Row : {idx}")
print(f"Failure Probability : {probs[idx]:.6f}")

# ----------------------------
# SHAP
# ----------------------------
explainer = shap.TreeExplainer(model)

explanation = explainer(sample)

print("\nExplanation object created.")

print("\nBase Values:")
print(explanation.base_values)

print("\nSHAP Values Shape:")
print(explanation.values.shape)

print("\nExpected Value:")
print(explainer.expected_value)

print("\nModel Probability:")
print(model.predict_proba(sample))

print("\nRaw SHAP values:")
print(explanation.values)
