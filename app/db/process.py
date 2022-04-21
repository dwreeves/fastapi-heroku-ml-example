import typing as t
from pathlib import Path

import pandas as pd

from app.config import settings
from app.db.core import AsyncSession
from app.db.models import Airport


async def seed_db(
        path: t.Union[Path, str] = settings.DEFAULT_AIRPORTS_CSV
) -> None:
    """Add data to the database."""

    async with AsyncSession() as db:

        data: t.List[t.Dict[str, t.Any]] = \
            pd.read_csv(path).to_dict(orient="records")

        for row in data:
            airport = Airport(**row)
            db.add(airport)

        await db.commit()
