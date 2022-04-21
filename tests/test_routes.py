import os.path as op
import typing as t

import orjson
import pytest


TEST_DIR = op.abspath(op.dirname(__file__))
REQUESTS_DIR = op.join(TEST_DIR, "resources", "requests")
RESPONSES_DIR = op.join(TEST_DIR, "resources", "responses")


@pytest.fixture
def request_response(request) -> t.Tuple[dict, dict]:
    with open(op.join(REQUESTS_DIR, f"{request.param}.json"), "r") as f:
        req = orjson.loads(f.read())
    with open(op.join(RESPONSES_DIR, f"{request.param}.json"), "r") as f:
        res = orjson.loads(f.read())
    return req, res


def request_response_pairs(*files: str) -> callable:
    return pytest.mark.parametrize(
        "request_response",
        files,
        indirect=["request_response"]
    )


@request_response_pairs(
    "e1_m1_basic_example",
    "e1_m1_non_international_us",
    "e1_m1_non_international_china",
    "e1_m1_two_predictions"
)
@pytest.mark.asyncio
async def test_endpoint_api_v1_model_v1(client, request_response, db):
    req, expected_res = request_response
    res = client.post("/api/v1/predict", json=req)
    assert res.status_code == 200
    assert res.json() == expected_res


@pytest.mark.asyncio
async def test_health_check(client):
    assert client.get("/healthz").status_code == 200
