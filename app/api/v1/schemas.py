import typing as t
from enum import Enum

from pydantic.main import BaseModel

from app.db.models import Airport


# ==========================================================
# Original request
# ==========================================================


class PreprocessedInstance(BaseModel):
    origin_iata: str
    destination_iata: str


class PreprocessedRequest(BaseModel):
    instances: t.List[PreprocessedInstance]


# ==========================================================
# Feature lookups
# ==========================================================


class ProcessedInstance(BaseModel):
    origin_airport: Airport
    destination_airport: Airport


class ProcessedRequest(BaseModel):
    instances: t.List[ProcessedInstance]


# ==========================================================
# Response
# ==========================================================


class Distance(BaseModel):
    value: float
    unit: t.Literal["km"] = "km"


class PredictionInstance(BaseModel):
    distance: Distance
    international: bool


class PredictionResponse(BaseModel):
    instances: t.List[PredictionInstance]
