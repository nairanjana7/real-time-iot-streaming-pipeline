import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

features = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

X = df[features]

model = IsolationForest(
    contamination=0.034,   # matches failure rate ~3.4%
    random_state=42
)

model.fit(X)

joblib.dump(model, "models/isolation_forest.pkl")

print("Model trained successfully")
