import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    auc
)

# Load dataset
df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

# -------------------------
# Feature Engineering
# -------------------------
df["Power"] = df["Torque [Nm]"] * df["Rotational speed [rpm]"]
df["Temp Difference"] = (
    df["Process temperature [K]"] - df["Air temperature [K]"]
)

# Encode machine type
df = pd.get_dummies(df, columns=["Type"])

# Features
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

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Weighted Random Forest
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Probabilities
y_probs = model.predict_proba(X_test)[:, 1]

# Threshold tuned for recall
threshold = 0.30
y_pred = (y_probs >= threshold).astype(int)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

precision, recall, _ = precision_recall_curve(y_test, y_probs)
pr_auc = auc(recall, precision)

print("\nPR-AUC:", pr_auc)

joblib.dump(model, "models/random_forest.pkl")
print("\nModel saved.")
