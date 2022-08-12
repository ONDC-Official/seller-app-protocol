import json

import requests
from main.config import get_config_by_name
from main.utils.webhook_utils import post_on_bg_or_bap


def send_bpp_responses_to_bg(request_type, payload):
    search_responses = get_responses_from_client(request_type, payload)
    post_on_bg_or_bap(payload['context']['bap_url'], search_responses)


def get_responses_from_client(request_type, payload):
    client_endpoint = get_config_by_name('CLIENT_ENDPOINT')
    response = requests.post(f"{client_endpoint}/{request_type}", json=payload)
    return json.loads(response.text)

