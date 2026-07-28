import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix

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
y_true = df["Machine failure"]

model = joblib.load("models/isolation_forest.pkl")

pred = model.predict(X)

# IsolationForest outputs:
# 1 = normal
# -1 = anomaly

pred = [1 if x == -1 else 0 for x in pred]

print("Confusion Matrix:")
print(confusion_matrix(y_true, pred))

print("\nClassification Report:")
print(classification_report(y_true, pred))
