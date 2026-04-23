from typing import Optional

import numpy as np
import mlflow.pyfunc
import pandas as pd

from wine_graphql_api.config import MLFLOW_TRACKING_URI, MODEL_NAME

# Claves que usa la API (alineadas con proto/REST). El modelo sklearn se entrena con
# sklearn.datasets.load_wine: la columna equivalente a od280_od315 se llama así:
_SKLEARN_OD280 = "od280/od315_of_diluted_wines"

# Nombres de columnas en el orden de load_wine(as_frame=True).frame (sin target).
_SKLEARN_COLUMNS = (
    "alcohol",
    "malic_acid",
    "ash",
    "alcalinity_of_ash",
    "magnesium",
    "total_phenols",
    "flavanoids",
    "nonflavanoid_phenols",
    "proanthocyanins",
    "color_intensity",
    "hue",
    _SKLEARN_OD280,
    "proline",
)

# Mismas posiciones que _SKLEARN_COLUMNS; la API usa od280_od315 como en el proto.
_API_KEYS = (
    "alcohol",
    "malic_acid",
    "ash",
    "alcalinity_of_ash",
    "magnesium",
    "total_phenols",
    "flavanoids",
    "nonflavanoid_phenols",
    "proanthocyanins",
    "color_intensity",
    "hue",
    "od280_od315",
    "proline",
)

_model: Optional[mlflow.pyfunc.PyFuncModel] = None


def load_model() -> mlflow.pyfunc.PyFuncModel:
    global _model
    if _model is None:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        _model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/latest")
    return _model


def predict_class(features: dict) -> int:
    model = load_model()
    row = {
        sk: features[api]
        for sk, api in zip(_SKLEARN_COLUMNS, _API_KEYS)
    }
    pdf = pd.DataFrame([row], columns=list(_SKLEARN_COLUMNS))
    out = model.predict(pdf)
    return int(np.asarray(out).ravel()[0])
