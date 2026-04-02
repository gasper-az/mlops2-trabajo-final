import grpc
import numpy as np
from concurrent import futures

from wine_grpc_server.model import load_model
from wine_grpc_server.config import GRPC_PORT

import wine_inference_pb2
import wine_inference_pb2_grpc

class WineInferenceService(
    wine_inference_pb2_grpc.WineInferenceServiceServicer
):
    def __init__(self):
        self.model = load_model()

    def Predict(self, request, context):
        features = np.array([[
            request.alcohol,
            request.malic_acid,
            request.ash,
            request.alcalinity_of_ash,
            request.magnesium,
            request.total_phenols,
            request.flavanoids,
            request.nonflavanoid_phenols,
            request.proanthocyanins,
            request.color_intensity,
            request.hue,
            request.od280_od315,
            request.proline
        ]])

        prediction = int(self.model.predict(features)[0])

        return wine_inference_pb2.PredictResponse(
            predicted_class=prediction,
            model_version="latest"
        )
    
def create_server():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    wine_inference_pb2_grpc.add_WineInferenceServiceServicer_to_server(
        WineInferenceService(),
        server
    )

    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    return server