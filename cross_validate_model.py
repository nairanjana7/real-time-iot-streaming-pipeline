import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    precision_recall_curve,
    auc
)

# Load dataset
df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

# Feature engineering
df["Power"] = df["Torque [Nm]"] * df["Rotational speed [rpm]"]
df["Temp Difference"] = (
    df["Process temperature [K]"] - df["Air temperature [K]"]
)

# Encode machine type
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

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

precision_scores = []
recall_scores = []
f1_scores = []
pr_auc_scores = []

fold = 1

for train_idx, test_idx in skf.split(X, y):
    print(f"\nRunning Fold {fold}...")

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    y_probs = model.predict_proba(X_test)[:, 1]

    threshold = 0.30
    y_pred = (y_probs >= threshold).astype(int)

    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    precision_curve, recall_curve, _ = precision_recall_curve(
        y_test,
        y_probs
    )

    pr_auc = auc(recall_curve, precision_curve)

    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    pr_auc_scores.append(pr_auc)

    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"PR-AUC:    {pr_auc:.4f}")

    fold += 1

print("\n========== FINAL RESULTS ==========")
print(
    f"Precision: {np.mean(precision_scores):.4f} ± {np.std(precision_scores):.4f}"
)
print(
    f"Recall:    {np.mean(recall_scores):.4f} ± {np.std(recall_scores):.4f}"
)
print(
    f"F1 Score:  {np.mean(f1_scores):.4f} ± {np.std(f1_scores):.4f}"
)
print(
    f"PR-AUC:    {np.mean(pr_auc_scores):.4f} ± {np.std(pr_auc_scores):.4f}"
)
