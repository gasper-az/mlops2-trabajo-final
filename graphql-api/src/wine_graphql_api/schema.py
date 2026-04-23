import strawberry

from wine_graphql_api.model import predict_class


@strawberry.input
class WineFeaturesInput:
    alcohol: float
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


@strawberry.type
class PredictResult:
    predicted_class: int
    model_version: str


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"


@strawberry.type
class Mutation:
    @strawberry.mutation
    def predict(self, features: WineFeaturesInput) -> PredictResult:
        payload = {
            "alcohol": features.alcohol,
            "malic_acid": features.malic_acid,
            "ash": features.ash,
            "alcalinity_of_ash": features.alcalinity_of_ash,
            "magnesium": features.magnesium,
            "total_phenols": features.total_phenols,
            "flavanoids": features.flavanoids,
            "nonflavanoid_phenols": features.nonflavanoid_phenols,
            "proanthocyanins": features.proanthocyanins,
            "color_intensity": features.color_intensity,
            "hue": features.hue,
            "od280_od315": features.od280_od315,
            "proline": features.proline,
        }
        predicted = predict_class(payload)
        return PredictResult(
            predicted_class=predicted,
            model_version="latest",
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
