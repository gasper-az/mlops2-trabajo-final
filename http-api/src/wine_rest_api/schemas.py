from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    alcohol: float = Field(..., example=13.2)
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315: float
    proline: float

class PredictResponse(BaseModel):
    predicted_class: int
    model_version: str