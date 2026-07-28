import pandas as pd

from ml.config import FEATURES


def preprocess_dataframe(df):
    """
    Apply the same preprocessing used during training.
    """

    df = df.copy()

    df["Power"] = (
        df["Torque [Nm]"] *
        df["Rotational speed [rpm]"]
    )

    df["Temp Difference"] = (
        df["Process temperature [K]"] -
        df["Air temperature [K]"]
    )

    df = pd.get_dummies(df, columns=["Type"])

    # Ensure all expected dummy columns exist
    for col in ["Type_H", "Type_L", "Type_M"]:
        if col not in df.columns:
            df[col] = 0

    return df[FEATURES]
