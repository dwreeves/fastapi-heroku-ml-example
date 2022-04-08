import asyncio
import typing as t

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.v1.schemas import PreprocessedRequest
from app.api.v1.schemas import PreprocessedInstance
from app.api.v1.schemas import ProcessedInstance
from app.api.v1.schemas import ProcessedRequest
from app.api.v1.schemas import PredictionResponse
from app.api.v1.core import DEFAULT_MODEL
from app.api.v1.core import predictive_models
from app.api.v1.core import PredictiveModelBase
from app.api.v1.core import PredictiveModelName
from app.db.core import get_db
from app.db.models import Airport


app = FastAPI(
    root_path="/api/v1"
)


async def process_instance(
        inst: PreprocessedInstance,
        db: AsyncSession
) -> ProcessedInstance:
    origin_airport = (await db.execute(
        select(Airport)
        .filter(Airport.iata == inst.origin_iata)
        .limit(1)
    )).scalar_one_or_none()
    destination_airport = (await db.execute(
        select(Airport)
        .filter(Airport.iata == inst.destination_iata)
        .limit(1)
    )).scalar_one_or_none()

    # Handle a bad request here.
    if origin_airport is None or destination_airport is None:
        msg = ""
        if origin_airport is None:
            msg += f"origin_iata {inst.origin_iata} is not valid."
        if destination_airport is None:
            msg += f" destination_iata {inst.destination_iata} is not valid."
        raise HTTPException(status_code=400, detail=msg.strip())

    return ProcessedInstance(
        origin_airport=origin_airport,
        destination_airport=destination_airport
    )


async def process_request(
        req: PreprocessedRequest,
        db: AsyncSession = Depends(get_db)
) -> ProcessedRequest:
    """Get data from where we are storing data."""
    # This is where the "feature store" goes.
    # In this case, "feature store" means Postgres.
    instances = await asyncio.gather(*[
        process_instance(inst=inst, db=db) for inst in req.instances
    ])
    return ProcessedRequest(instances=instances)


def get_predictive_model(
        model: PredictiveModelName = DEFAULT_MODEL
) -> PredictiveModelBase:
    try:
        return predictive_models[model]
    except KeyError:
        raise HTTPException(status_code=404, detail="Model not found")


@app.post("/predict")
async def predict_view(
        data: ProcessedRequest = Depends(process_request),
        predictive_model: PredictiveModelBase = Depends(get_predictive_model)
) -> PredictionResponse:
    """Run a prediction (calculate distance)."""
    instances = []
    for d in data.instances:
        inst = predictive_model.predict(d)
        instances.append(inst)
    return PredictionResponse(instances=instances)
