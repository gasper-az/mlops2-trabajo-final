import numpy as np

from wine_grpc_server.config import (
    FEATURE_ORDER,
    OOD_HIGH,
    OOD_LOW,
    OOD_STATS_PATH
)

ref = np.load(OOD_STATS_PATH)

MU = ref["mean"]
INV_COV = ref["inv_cov"]

def mahalanobis_distance(x):
    d = x - MU
    return float((d @ INV_COV @ d.T) ** 0.5)

def compute_ood(features: dict):
    x = np.array([features[f] for f in FEATURE_ORDER])
    score = mahalanobis_distance(x)

    if score >= OOD_HIGH:
        severity = "HIGH"
    elif score >= OOD_LOW:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return score, severity