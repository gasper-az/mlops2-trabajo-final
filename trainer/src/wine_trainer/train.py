import mlflow
import mlflow.sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from wine_trainer.config import (
    EXPERIMENT_NAME,
    MLFLOW_TRACKING_URI,
    MODEL_NAME,
    OOD_STATS_PATH,
    RANDOM_STATE,
    TEST_SIZE
)
from wine_trainer.data import load_dataset
from wine_trainer.ood import save_ood_stats
from wine_trainer.stats import compute_reference_stats

def main() -> None:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    df = load_dataset()
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    model = LogisticRegression(
        max_iter=500,
        random_state=RANDOM_STATE
    )

    model.fit(X_train, y_train)

    # Evaluacion
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    f1 = f1_score(y_true=y_test, y_pred=y_pred, average="weighted")

    reference_stats = compute_reference_stats(X_train)

    with mlflow.start_run():
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)

        mlflow.log_params({
            "model_type": "LogisticRegression",
            "max_iter": 500,
            "test_size": TEST_SIZE
        })

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=MODEL_NAME,
            registered_model_name=MODEL_NAME
        )

        mlflow.log_dict(
            reference_stats,
            "reference_stats.json"
        )

    print("Training completed!!!")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1-score: {f1:.4f}")

    save_ood_stats(X_train=X_train, path=OOD_STATS_PATH)
    print("OOD reference saved!!!")

if __name__ == "__main__":
    main()