from typing import List
from uuid import uuid4
from time import time, sleep
import pytest
from smoke import conftest
from aiohttp import ClientResponse
from api_test_utils import env
from api_test_utils import poll_until
from api_test_utils.api_session_client import APISessionClient
from api_test_utils.api_test_session_config import APITestSessionConfig


def dict_path(raw, path: List[str]):
    if not raw:
        return raw

    if not path:
        return raw

    res = raw.get(path[0])
    if not res or len(path) == 1 or type(res) != dict:
        return res

    return dict_path(res, path[1:])

def _base_valid_uri(nhs_number) -> str:
    return f"FHIR/R4/Observation?patient.identifier=https://fhir.nhs.uk/Id/nhs-number|{nhs_number}"


def _valid_uri(nhs_number, procedure_code) -> str:
    return _base_valid_uri(nhs_number) + f"&procedure-code:below={procedure_code}"


@pytest.fixture(scope='function')
def authorised_headers(valid_access_token):
    return {"Authorization": f"Bearer {valid_access_token}"}


@pytest.mark.e2e
@pytest.mark.smoketest
@pytest.mark.asyncio
async def test_check_observation_is_secured(api_client: APISessionClient):

    async with api_client.get(_base_valid_uri("0000000001"), allow_retries=True) as resp:
        assert resp.status == 401


@pytest.mark.e2e
@pytest.mark.smoketest
@pytest.mark.asyncio
async def test_observation_happy_path(test_app, api_client: APISessionClient, authorised_headers):

    correlation_id = str(uuid4())
    authorised_headers["X-Correlation-ID"] = correlation_id
    authorised_headers["NHSD-User-Identity"] = conftest.nhs_login_id_token(test_app)

    async with api_client.get(
        _base_valid_uri("0000000001"),
        headers=authorised_headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 200
        body = await resp.json()
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
        assert body["resourceType"] == "Bundle", body
        # TODO verify data
        # assert len(body["entry"]) == 0, body

@pytest.mark.smoketestsandbox
@pytest.mark.asyncio
async def test_observation_happy_path_sandbox(test_app, api_client: APISessionClient, authorised_headers):

    correlation_id = str(uuid4())
    authorised_headers["X-Correlation-ID"] = correlation_id
    authorised_headers["NHSD-User-Identity"] = conftest.nhs_login_id_token(test_app)

    async with api_client.get(
        _base_valid_uri("0000000001"),
        headers=authorised_headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 200
        body = await resp.json()
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
        assert body["resourceType"] == "Bundle", body
        # TODO verify data
        # assert len(body["entry"]) == 0, body
