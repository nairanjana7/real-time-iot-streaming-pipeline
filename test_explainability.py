import pandas as pd

from ml.preprocessing import preprocess_dataframe
from ml.predictor import FailurePredictor
from ml.explainability import ExplainabilityEngine

df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

sample = df.iloc[[50]]

sample = preprocess_dataframe(sample)

predictor = FailurePredictor()

model = predictor.get_model()

engine = ExplainabilityEngine(model)

explanation = engine.explain(sample)

print("Base Values:")
print(explanation.base_values)

print()

print("SHAP Shape:")
print(explanation.values.shape)
