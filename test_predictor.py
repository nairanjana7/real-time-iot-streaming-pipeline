import pandas as pd

from ml.preprocessing import preprocess_dataframe
from ml.predictor import FailurePredictor

df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

sample = df.iloc[[50]]

sample = preprocess_dataframe(sample)

predictor = FailurePredictor()

prediction, probability = predictor.predict(sample)

print("Prediction:", prediction)
print("Probability:", probability)
