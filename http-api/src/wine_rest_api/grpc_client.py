import grpc

from wine_inference_pb2 import PredictRequest
from wine_inference_pb2_grpc import WineInferenceServiceStub

from wine_rest_api.config import (
    GRPC_SERVER_HOST,
    GRPC_SERVER_PORT
)

class GrpcInferenceClient:
    def __ini__(self):
        target = f"{GRPC_SERVER_HOST}:{GRPC_SERVER_PORT}"
        self.channel = grpc.insecure_channel(target)
        self.stub = WineInferenceServiceStub(self.channel)

    def predict(self, payload: dict):
        request = PredictRequest(**payload)
        response = self.stub.Predict(request)
        return response