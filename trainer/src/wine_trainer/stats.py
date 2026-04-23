import pandas as pd

def compute_reference_stats(df: pd.DataFrame) -> dict:
    return {
        column: {
            "mean": float(df[column].mean()),
            "std": float(df[column].std()),
            "min": float(df[column].min()),
            "max": float(df[column].max()),
        }
        for column in df.columns
    }