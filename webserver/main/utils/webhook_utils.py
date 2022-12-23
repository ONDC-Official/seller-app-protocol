import json

import requests
from retry import retry

from main.config import get_config_by_name
from main.logger.custom_logging import log


@retry(tries=3, delay=1)
def requests_post_with_retries(url, payload, headers=None):
    response = requests.post(url, json=payload, headers=headers)
    status_code = response.status_code
    if status_code != 200:
        raise requests.exceptions.HTTPError("Request Failed!")
    return status_code


def requests_post(url, raw_data, headers=None):
    response = requests.post(url, data=raw_data, headers=headers)
    return response.text, response.status_code


def post_on_bg_or_bap(url, payload, headers={}):
    headers.update({'Content-Type': 'application/json'})
    raw_data = json.dumps(payload, separators=(',', ':'))
    response_text, status_code = requests_post(url, raw_data, headers=headers)
    log(response_text)
    return status_code


def lookup_call(url, payload, headers=None):
    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.text), response.status_code
