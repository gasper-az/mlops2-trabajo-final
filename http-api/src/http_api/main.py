from fastapi import FastAPI
from pydantic import BaseModel, Field
from http_api.grpc_client import GrpcPredictionClient

app = FastAPI(title="REST Prediction API")

grpc_client = GrpcPredictionClient()

class PredictRequest(BaseModel):
    features: list[float] = Field(..., example=[5.1, 3.5, 1.4, 0.2])

class PredictResponse(BaseModel):
    prediction: float

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    prediction = grpc_client.predict(request.features)
    return PredictResponse(prediction=prediction)