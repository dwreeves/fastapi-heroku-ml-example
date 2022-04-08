import sqlalchemy as sa
from sqlmodel import SQLModel
from sqlmodel import Field
from app.db.core import Base


class Airport(SQLModel, table=True):
    # In a more robust production system, you'd want to represent airports as a
    # slowly changing dimension. Here, a denormalized flat table is fine for
    # demo purposes.
    iata: str = Field(primary_key=True, index=True)
    latitude: float
    longitude: float
    country_code: str
