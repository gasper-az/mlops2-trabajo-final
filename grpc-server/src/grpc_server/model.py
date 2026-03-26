from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import numpy as np

class IrisLogisticRegressionModel:
    def __init__(self) -> None:
        self.model = LogisticRegression(
            solver="lbfgs",
            max_iter=200
        )
        self._train()
    
    def _train(self) -> None:
        X, y = load_iris(return_X_y=True)
        self.model.fit(X, y)
    
    def predict(self, features: list[float]) -> int:
        features_array = np.array(features).reshape(1, -1)
        prediction = self.model.predict(features_array)
        return int(prediction[0])
        # Alternativa 1
        # target_names = ["setosa", "versicolor", "virginica"]
        # return target_names[prediction[0]]
        ######################################################
        # Alternativa 2
        # proba = self.model.predict_proba(features_array)[0]
        # return target_names[prediction[0]]
        ## Adem'as, hay que actualizar el proto file
        # message PredictResponse {
        #   repeated float probabilities = 1;
        # }