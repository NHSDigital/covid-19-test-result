import sys
import requests
# from lxml import html
from urllib.parse import urlparse, parse_qs
from ast import literal_eval
import os

ENVIRONMENT = "internal-dev"

client_id = os.environ["NHS_Login_Client_Id"] #"YOUR_CLIENT_ID_HERE"
client_secret = os.environ["NHS_Login_Client_secret"] #"YOUR_CLIENT_SECRET_HERE"
redirect_uri = "https://example.org/callback" # Must match your app...

base_path = "oauth2"
if ENVIRONMENT == "int":
    base_path = "oauth2-no-smartcard"
identity_service_url = f"https://{ENVIRONMENT}.api.service.nhs.uk/{base_path}"

def main():
    resp = requests.get(f"{identity_service_url}/authorize",
                        params = {
                            'client_id': client_id,
                            'redirect_uri': redirect_uri,
                            'response_type':'code',
                            'state': '1234567890'
                        })

    if resp.status_code != 200:
        print(resp.content.decode())
        sys.exit(1)

    tree = html.fromstring(resp.content.decode())

    state = None
    for form in tree.body:
        assert form.tag == "form"
        input_elems = [item for item in form if item.tag == "input"]
        state = dict(input_elems[0].items())['value']

    resp2 = requests.post(f"{identity_service_url}/simulated_auth",
                          data={"state": state})

    if "herokuapp" in redirect_uri:
        # Then the herokuapp has done the POST and so we can parse and results
        tree2 = html.fromstring(resp2.content.decode())
        for div in tree2.body:
            assert div.tag == "div"
            for div in div:
                assert div.tag == "div"
                data_items = [item for item in div if item.tag == "pre"]
                result = literal_eval(data_items[0].text)
                return result['access_token']
    else:
        # We do the POST identity-service expects ourselves
        qs = urlparse(resp2.history[-1].headers['Location']).query

        auth_code = parse_qs(qs)['code']
        if isinstance(auth_code, list):
            auth_code = auth_code[0]

        resp3 = requests.post(f"{identity_service_url}/token",
                              data = {
                                  'grant_type': 'authorization_code',
                                  'code': auth_code,
                                  'redirect_uri': redirect_uri,
                                  'client_id': client_id,
                                  'client_secret': client_secret,
                              })
        return resp3.json()['access_token']


if __name__ == '__main__':
    data = main()
    print(data)
