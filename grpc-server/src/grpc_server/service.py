from generated.prediction_pb2 import PredictResponse
from generated.prediction_pb2_grpc import PredictionServiceServicer
from grpc_server.model import IrisLogisticRegressionModel

class PredictionService(PredictionServiceServicer):
    def __init__(self) -> None:
        self.model = IrisLogisticRegressionModel()
    
    def Predict(self, request, context):
        features = list(request.features)
        prediction = self.model.predict(features=features)
        return PredictResponse(prediction=prediction)