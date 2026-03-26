import grpc
from generated.prediction_pb2 import PredictRequest
from generated.prediction_pb2_grpc import PredictionServiceStub

class GrpcPredictionClient:
    def __init__(self, host: str = "grpc-server", port: int = 50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = PredictionServiceStub(self.channel)
    
    def predict(self, features: list[float]) -> float:
        request = PredictRequest(features=features)
        response = self.stub.Predict(request)
        return response.prediction