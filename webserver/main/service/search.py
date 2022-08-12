import json

import requests
from main.config import get_config_by_name
from main.utils.webhook_utils import post_on_bg_or_bap


def send_search_catalogs_to_bg(payload):
    search_responses = get_search_catalogs_from_client(payload)
    post_on_bg_or_bap(payload['context']['bap_url'], search_responses)


def get_search_catalogs_from_client(payload):
    client_endpoint = get_config_by_name('CLIENT_ENDPOINT')
    response = requests.post(f"{client_endpoint}/search", json=payload)
    return json.loads(response.text)

