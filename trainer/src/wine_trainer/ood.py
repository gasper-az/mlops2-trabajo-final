import numpy as np
import pandas as pd

def save_ood_stats(X_train: pd.DataFrame, path: str):
    mu = X_train.mean(axis=0)
    cov = np.cov(X_train, rowvar=False)

    np.savez(
        path,
        mean=mu,
        inv_cov=np.linalg.inv(cov)
    )