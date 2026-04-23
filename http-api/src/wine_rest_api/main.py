from fastapi import FastAPI
from wine_rest_api.grpc_client import GrpcInferenceClient
from wine_rest_api.schemas import (
    PredictRequest,
    PredictResponse
)

app = FastAPI(
    title="Clasificador de Vinos",
    version="1.0.0"
)

grpc_client = GrpcInferenceClient()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    response = grpc_client.predict(request.dict())
    return PredictResponse(
        predicted_class=response.predicted_class,
        model_version=response.model_version
    )