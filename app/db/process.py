import os.path as op
import typing as t

import pandas as pd

from app.db.core import AsyncSession
from app.db.models import Airport

AIRPORTS_CSV = op.join(op.dirname(__file__), "data", "airports_v1.csv")


async def seed_db() -> None:
    """Add data to the database."""

    async with AsyncSession() as db:

        data: t.List[t.Dict[str, t.Any]] = \
            pd.read_csv(AIRPORTS_CSV).to_dict(orient="records")

        for row in data:
            airport = Airport(**row)
            db.add(airport)

        await db.commit()
