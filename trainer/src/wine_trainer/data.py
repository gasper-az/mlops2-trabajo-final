import pandas as pd
from sklearn.datasets import load_wine

def load_dataset() -> pd.DataFrame:
    wine = load_wine(as_frame=True)
    df = wine.frame.copy()
    df["target"] = wine.target
    return df