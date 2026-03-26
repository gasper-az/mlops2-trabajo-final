from concurrent import futures
import grpc

from generated.prediction_pb2_grpc import (
    add_PredictionServiceServicer_to_server,
)
from grpc_server.service import PredictionService

def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PredictionServiceServicer_to_server(
        PredictionService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server escuchando en el puerto 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()