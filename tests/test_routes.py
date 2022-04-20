import pytest


def requests(*files: str) -> callable:
    return pytest.mark.parametrize(
        "request_response",
        files,
        indirect=["request_response"]
    )


@requests(
    "basic_example",
    "non_international_us",
    "non_international_china"
)
@pytest.mark.asyncio
async def test_endpoint_api_v1_model_v1(client, request_response, db):
    req, expected_res = request_response
    res = client.post("/api/v1/predict", json=req).json()
    assert res == expected_res
