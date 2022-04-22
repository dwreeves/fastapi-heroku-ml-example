import math
import typing as t
from enum import Enum

from numba import float32
from numba import jit

from app.api.v1.schemas import Distance
from app.api.v1.schemas import PredictionInstance
from app.api.v1.schemas import ProcessedInstance


class PredictiveModelName(str, Enum):
    v1 = "v1"
    v2 = "v2"


DEFAULT_MODEL = PredictiveModelName.v2


class PredictiveModelBase(t.Protocol):
    name: str = None

    def predict(self, data: ProcessedInstance) -> PredictionInstance:
        raise NotImplementedError


class PredictiveModelV1(PredictiveModelBase):
    name = "v1"

    def predict(self, data: ProcessedInstance) -> PredictionInstance:
        """V1 is a really terrible model.
        Just returns heuristic answers.
        """
        return PredictionInstance(
            distance={"value": 1000, "unit": "km"},
            international=False
        )


class PredictiveModelV2(PredictiveModelBase):
    name = "v2"

    @staticmethod
    @jit(float32(float32, float32, float32, float32), nopython=True)
    def _haversine_distance(
            lat1: float,
            lat2: float,
            lon1: float,
            lon2: float,
    ) -> float:
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            (math.sin(dlat / 2) ** 2) +
            math.cos(math.radians(lat1)) *
            math.cos(math.radians(lat2)) *
            (math.sin(dlon / 2) ** 2)
        )
        dist = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) * 6371
        return dist

    def predict(self, data: ProcessedInstance) -> PredictionInstance:
        """V2 is a slightly better model.

        Derived from: https://stackoverflow.com/a/38187562
        """

        # Calculate distance

        dist = self._haversine_distance(
            lat1=data.origin_airport.latitude,
            lon1=data.origin_airport.longitude,
            lat2=data.destination_airport.latitude,
            lon2=data.destination_airport.longitude
        )

        # Calculate if it's international.

        origin_cc = data.origin_airport.country_code
        destination_cc = data.destination_airport.country_code
        international = bool(origin_cc != destination_cc)

        return PredictionInstance(
            distance=Distance(value=dist),
            international=international
        )


predictive_models: t.Dict[PredictiveModelName, PredictiveModelBase] = {
    PredictiveModelName.v1: PredictiveModelV1(),
    PredictiveModelName.v2: PredictiveModelV2()
}
