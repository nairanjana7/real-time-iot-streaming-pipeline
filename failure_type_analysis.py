import pandas as pd
from sklearn.model_selection import train_test_split
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

X_train, X_test, y_train, y_test, train_indices, test_indices = train_test_split(
    X,
    y,
    df.index,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

y_probs = model.predict_proba(X_test)[:, 1]
threshold = 0.30
y_pred = (y_probs >= threshold).astype(int)

test_df = df.loc[test_indices].copy()
test_df["predicted_failure"] = y_pred

failure_types = ["TWF", "HDF", "PWF", "OSF", "RNF"]

for failure in failure_types:
    subset = test_df[test_df[failure] == 1]

    total = len(subset)

    if total == 0:
        print(f"{failure}: No samples")
        continue

    detected = subset["predicted_failure"].sum()
    recall = detected / total

    print(
        f"{failure}: detected {detected}/{total} "
        f"(Recall={recall:.4f})"
    )
