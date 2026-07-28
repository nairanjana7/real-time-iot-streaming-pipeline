import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

# Feature engineering
df["Power"] = df["Torque [Nm]"] * df["Rotational speed [rpm]"]
df["Temp Difference"] = (
    df["Process temperature [K]"] - df["Air temperature [K]"]
)

# One-hot encoding
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
y = df["Machine failure"]

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X, y)

importances = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print(importance_df)
