import os.path as op
import typing as t

import pandas as pd

from app.db.core import AsyncSession
from app.db.models import Airport

AIRPORTS_CSV = op.join(op.dirname(__file__), "airports.csv")


async def seed_db() -> None:
    """Add data to the database."""

    async with AsyncSession() as session:
        data: t.List[t.Dict[str, t.Any]] = \
            pd.read_csv(AIRPORTS_CSV).to_dict(orient="records")

        for row in data:
            airport = Airport(**row)
            session.add(airport)

        await session.commit()
