import grpc
import numpy as np
from concurrent import futures

from wine_grpc_server.config import (
    GRPC_PORT,
    MODEL_NAME
)
from wine_grpc_server.kafka_producer import (
    publish_inference_event,
    publish_ood_event
)
from wine_grpc_server.model import load_model
from wine_grpc_server.ood import compute_ood
from wine_grpc_server.postgres import persist_ood_alert

import wine_inference_pb2
import wine_inference_pb2_grpc

# Se asegura la creacion de la tabla

class WineInferenceService(
    wine_inference_pb2_grpc.WineInferenceServiceServicer
):
    def __init__(self):
        self.model = load_model()

    def Predict(self, request, context):
        features = {
            "alcohol": request.alcohol,
            "malic_acid": request.malic_acid,
            "ash": request.ash,
            "alcalinity_of_ash": request.alcalinity_of_ash,
            "magnesium": request.magnesium,
            "total_phenols": request.total_phenols,
            "flavanoids": request.flavanoids,
            "nonflavanoid_phenols": request.nonflavanoid_phenols,
            "proanthocyanins": request.proanthocyanins,
            "color_intensity": request.color_intensity,
            "hue": request.hue,
            "od280_od315": request.od280_od315,
            "proline": request.proline,
        }

        score, severity = compute_ood(features=features)

        prediction = int(self.model.predict(
            [[*features.values()]]
        )[0])

        publish_inference_event(
            features=features,
            model_name=MODEL_NAME,
            prediction=prediction
        )

        publish_ood_event(
            model_name=MODEL_NAME,
            score=score
        )

        persist_ood_alert(
            model_name=MODEL_NAME,
            score=score,
            severity=severity
        )

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