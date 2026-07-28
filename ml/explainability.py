import shap


class ExplainabilityEngine:

    def __init__(self, model):

        self.explainer = shap.TreeExplainer(model)

    def explain(self, X):

        explanation = self.explainer(X)

        return explanation
