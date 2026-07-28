import joblib

from ml.config import MODEL_PATH


class FailurePredictor:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, X):
        """
        Returns:
        prediction (0/1)
        probability (0-1)
        """

        prediction = self.model.predict(X)[0]

        probability = self.model.predict_proba(X)[0][1]

        return prediction, probability

    def get_model(self):
        return self.model
