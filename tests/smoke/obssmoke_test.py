from typing import List
from uuid import uuid4
from time import time
import asyncio
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

def assert_body(body):
    assert body["resourceType"] == "Bundle", body
    assert len(body["entry"]) == 1
    assert body["entry"][0]["resource"]["resourceType"] == "Observation"
    assert body["entry"][0]["resource"]["id"] == "FAKEFORTESTS1"
    assert body["entry"][0]["resource"]["code"]["coding"][0]["code"] == "871555000"
    assert body["entry"][0]["resource"]["subject"]["reference"] == "Patient/9999999990"
    assert body["entry"][0]["resource"]["effectiveDateTime"] == "2021-05-29T13:23:10.000Z"
    assert body["entry"][0]["resource"]["valueCodeableConcept"]["coding"][0]["code"] == "1321691000000102"
    assert body["entry"][0]["resource"]["valueCodeableConcept"]["text"] == "SARS-CoV-2-ORGU"
    assert body["entry"][0]["resource"]["identifier"][0]["value"] == "FAKEFORTESTS1"
    assert body["entry"][0]["resource"]["device"]["identifier"]["value"] == "rtPCR"
    assert body["entry"][0]["resource"]["device"]["display"] == "rtPCR"
    assert body["entry"][0]["resource"]["performer"][0]["type"] == "Organization"
    assert body["entry"][0]["resource"]["performer"][0]["identifier"]["value"] == "NP"
    assert body["entry"][0]["resource"]["extension"][0]["extension"][1]["url"] == "administrationMethod"
    assert body["entry"][0]["resource"]["extension"][0]["extension"][1]["valueCodeableConcept"]["text"] == "health_care_professional"

@pytest.fixture(scope='function')
def authorised_headers(valid_access_token):
    return {"Authorization": f"Bearer {valid_access_token}"}


@pytest.mark.e2etest
@pytest.mark.smoketest
@pytest.mark.asyncio
async def test_check_observation_is_secured(api_client: APISessionClient):

    async with api_client.get(_base_valid_uri("9999999990"), allow_retries=True) as resp:
        assert resp.status == 401


# @pytest.mark.e2etest
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     'test_app',
#     [
#         {
#             'suffixes': ['-application-restricted']
#         },
#         {
#             'suffixes': ['-application-restricted', '-user-restricted']
#         }
#     ],
#     indirect=True
# )
# async def test_client_credentials_happy_path(test_app, api_client: APISessionClient):
#     authorised_headers = await conftest.get_authorised_headers(test_app)

#     correlation_id = str(uuid4())
#     authorised_headers["X-Correlation-ID"] = correlation_id

#     async with api_client.get(
#         _base_valid_uri("9999999990"),
#         headers=authorised_headers,
#         allow_retries=True
#     ) as resp:
#         assert resp.status == 200
#         body = await resp.json()
#         assert "x-correlation-id" in resp.headers, resp.headers
#         assert resp.headers["x-correlation-id"] == correlation_id
#         assert_body(body)

@pytest.mark.e2etest
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_app',
    [
        {
            'suffixes': ['-user-restricted']
        },
        {
            'suffixes': ['-application-restricted']
        }
    ],
    indirect=True
)
async def test_no_auth_bearer_token_provided(test_app, api_client: APISessionClient):
    await asyncio.sleep(1)  # Add delay to tests to avoid 429 on service callout
    correlation_id = str(uuid4())
    headers = {
        "Authorization": "Bearer",
        "X-Correlation-ID": correlation_id
    }
    async with api_client.get(
        _base_valid_uri("9999999990"),
        headers=headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 401, 'failed getting backend data'
        body = await resp.json()
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
        assert body["issue"] == [
            {'code': 'forbidden', 'diagnostics': 'Provided access token is invalid', 'severity': 'error'}
            ], body

# @pytest.mark.e2etest
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     'test_app',
#     [
#         {
#             'suffixes': ['-user-restricted'],
#             'requested_proofing_level': 'P9',
#             'identity_proofing_level': 'P9'
#         },
#         {
#             'suffixes': ['-user-restricted'],
#             'requested_proofing_level': 'P5',
#             'identity_proofing_level': 'P9'
#         },
#         {
#             'suffixes': ['-user-restricted'],
#             'requested_proofing_level': 'P5',
#             'identity_proofing_level': 'P5'
#         },
#         {
#             'suffixes': ['-application-restricted', '-user-restricted'],
#             'requested_proofing_level': 'P9',
#             'identity_proofing_level': 'P9'
#         },
#         {
#             'suffixes': ['-application-restricted', '-user-restricted'],
#             'requested_proofing_level': 'P5',
#             'identity_proofing_level': 'P9'
#         },
#         {
#             'suffixes': ['-application-restricted', '-user-restricted'],
#             'requested_proofing_level': 'P5',
#             'identity_proofing_level': 'P5'
#         }
#     ],
#     indirect=True
# )
# async def test_token_exchange_happy_path(test_app, api_client: APISessionClient):
#     subject_token_claims = {
#         'identity_proofing_level': test_app.request_params.get('identity_proofing_level')
#     }
#     token_response = await conftest.get_token_nhs_login_token_exchange(
#         test_app,
#         subject_token_claims=subject_token_claims
#     )
#     token = token_response["access_token"]

#     correlation_id = str(uuid4())
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "X-Correlation-ID": correlation_id
#     }

#     async with api_client.get(
#         _base_valid_uri("9999999990"),
#         headers=headers,
#         allow_retries=True
#     ) as resp:
#         assert resp.status == 200, 'failed getting backend data'
#         body = await resp.json()
#         assert "x-correlation-id" in resp.headers, resp.headers
#         assert resp.headers["x-correlation-id"] == correlation_id
#         assert_body(body)

@pytest.mark.smoketestsandbox
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_app',
    [
        {
            'suffixes': ['-application-restricted']
        },
        {
            'suffixes': ['-application-restricted', '-user-restricted']
        }
    ],
    indirect=True
)
async def test_observation_happy_path_sandbox(test_app, api_client: APISessionClient):
    authorised_headers = {}
    correlation_id = str(uuid4())
    authorised_headers["X-Correlation-ID"] = correlation_id

    async with api_client.get(
        _base_valid_uri("9999999990"),
        headers=authorised_headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 200
        body = await resp.json()
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
        assert body["resourceType"] == "Bundle", body
        assert len(body["entry"]) == 2
        assert body["entry"][0]["resource"]["resourceType"] == "Observation"
        assert body["entry"][0]["resource"]["id"] == "ASD32145123"
        assert body["entry"][0]["resource"]["code"]["coding"][0]["code"] == "871562009"
        assert body["entry"][0]["resource"]["subject"]["reference"] == "Patient/9999999990"
        assert body["entry"][0]["resource"]["valueCodeableConcept"]["coding"][0]["code"] == "1240581000000104"
        assert body["entry"][0]["resource"]["device"]["identifier"]["value"] == "rtPCR"
        assert body["entry"][0]["resource"]["device"]["display"] == "rtPCR"

# @pytest.mark.e2etest
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     'test_product_and_app',
#     [
#         {
#             'scopes': ['urn:nhsd:apim:user-nhs-login:P8:covid-19-test-result'],
#             'requested_proofing_level': 'P9',
#             'identity_proofing_level': 'P8'
#         }
#     ],
#     indirect=True
# )
# async def test_token_exchange_invalid_identity_proofing_level_scope(api_client: APISessionClient, test_product_and_app):

#     test_product, test_app = test_product_and_app
#     subject_token_claims = {
#         "identity_proofing_level": "P8"
#     }
#     token_response = await conftest.get_token_nhs_login_token_exchange(
#         test_app,
#         subject_token_claims=subject_token_claims
#     )
#     token = token_response["access_token"]

#     correlation_id = str(uuid4())
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "X-Correlation-ID": correlation_id
#     }

#     async with api_client.get(
#         _base_valid_uri("9999999990"),
#         headers=headers,
#         allow_retries=True
#     ) as resp:
#         assert resp.status == 401
#         body = await resp.json()
#         assert "x-correlation-id" in resp.headers, resp.headers
#         assert resp.headers["x-correlation-id"] == correlation_id
#         assert body == {
#             "issue":
#                 [
#                     {
#                         "severity": "error",
#                         "diagnostics": "Provided access token is invalid",
#                         "code": "forbidden"
#                     }
#                 ],
#             "resourceType": "OperationOutcome"
#         }

# @pytest.mark.e2etest
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     'test_product_and_app',
#     [
#         {
#             'scopes': ['urn:nhsd:apim:user-nhs-login:P9:covid-19-test-result'],
#             'requested_proofing_level': 'P9',
#             'identity_proofing_level': 'P9'
#         },
#         {
#             'scopes': ['urn:nhsd:apim:user-nhs-login:P5:covid-19-test-result'],
#             'requested_proofing_level': 'P5',
#             'identity_proofing_level': 'P5'
#         }
#     ],
#     indirect=True
# )
# async def test_token_exchange_both_header_and_exchange(api_client: APISessionClient,
#                                                        test_product_and_app):
#     test_product, test_app = test_product_and_app
#     subject_token_claims = {
#         'identity_proofing_level': test_app.request_params.get('identity_proofing_level')
#     }
#     authorised_headers = {}
#     correlation_id = str(uuid4())
#     authorised_headers["X-Correlation-ID"] = correlation_id
#     authorised_headers["NHSD-User-Identity"] = conftest.nhs_login_id_token(test_app)

#     # Use token exchange token in conjunction with JWT header
#     token_response = await conftest.get_token_nhs_login_token_exchange(
#         test_app,
#         subject_token_claims=subject_token_claims
#     )
#     token = token_response["access_token"]

#     authorised_headers["Authorization"] = f"Bearer {token}"

#     async with api_client.get(
#         _base_valid_uri("9999999990"),
#         headers=authorised_headers,
#         allow_retries=True
#     ) as resp:
#         assert resp.status == 200
#         body = await resp.json()
#         assert "x-correlation-id" in resp.headers, resp.headers
#         assert resp.headers["x-correlation-id"] == correlation_id
#         assert_body(body)
