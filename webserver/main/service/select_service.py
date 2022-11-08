import json
import time

import pika

from main import constant
from main.config import get_config_by_name
from main.logger.custom_logging import log
from main.models import get_mongo_collection
from main.repository import mongo
from main.service import send_message_to_queue_for_given_request
from main.service.common import get_responses_from_client
from main.utils.cryptic_utils import create_authorisation_header
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap

rabbitmq_connection, rabbitmq_channel = None, None


def make_logistics_search_request(payload):
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup()
    url_with_route = f"{gateway_or_bap_endpoint}{payload['context']['action']}" \
        if gateway_or_bap_endpoint.endswith("/") \
        else f"{gateway_or_bap_endpoint}/{payload['context']['action']}"
    auth_header = create_authorisation_header(payload)
    status_code = post_on_bg_or_bap(url_with_route, payload, headers={'Authorization': auth_header})
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_select_request_to_client(select_payload):
    return get_responses_from_client("select", select_payload)


def make_logistics_search_payload_request_to_client(select_payload):
    return get_responses_from_client("logistics/search", select_payload)


def send_on_select_to_bap(url_with_route, payload):
    auth_header = create_authorisation_header(payload)
    status_code = post_on_bg_or_bap(url_with_route, payload, headers={'Authorization': auth_header})
    # import requests
    # status_code = requests.post(url_with_route, json=payload, headers={'Authorization': auth_header})
    log(f"Sent responses to bg/bap with status-code {status_code}")


@check_for_exception
def make_logistics_search_or_send_bpp_failure_response(message):
    log(f"select_1 payload: {message}")
    select_message_id = message['message_ids']['select']
    select_collection = get_mongo_collection('select')
    select_payload = mongo.collection_find_one(select_collection, {"context.message_id": select_message_id})
    search_payload_or_select_response, return_code = make_logistics_search_payload_request_to_client(select_payload)
    if return_code == 200:
        search_message_id = search_payload_or_select_response[constant.CONTEXT]['message_id']
        make_logistics_search_request(search_payload_or_select_response)
        message['request_type'] = "select_2"
        message['message_ids']['logistics_search'] = search_message_id
        send_message_to_queue_for_given_request(message,
                                                properties=pika.BasicProperties(headers={
                                                    "x-delay": get_config_by_name("LOGISTICS_ON_SEARCH_WAIT")*1000,
                                                }))
    else:
        bap_endpoint = select_payload['context']['bap_uri']
        url_with_route = f"{bap_endpoint}on_select" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_select"
        send_on_select_to_bap(url_with_route, search_payload_or_select_response)


@check_for_exception
def send_select_response_to_bap(message):
    log(f"select_2 payload: {message}")
    select_message_id = message['message_ids']['select']
    logistics_search_message_id = message['message_ids']['logistics_search']
    select_collection = get_mongo_collection('select')
    logistics_search_collection = get_mongo_collection('logistics_on_search')
    payload = {
        "select": mongo.collection_find_one(select_collection, {"context.message_id": select_message_id}),
        "logistic_on_search": mongo.collection_find_all(logistics_search_collection,
                                                       {"context.message_id": logistics_search_message_id})
    }
    select_resp, return_code = make_select_request_to_client(payload)

    bap_endpoint = select_resp['context']['bap_uri']
    url_with_route = f"{bap_endpoint}on_select" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_select"
    send_on_select_to_bap(url_with_route, select_resp)


if __name__ == "__main__":
    search_payload_or_select_response1 = make_logistics_search_payload_request_to_client({})
    post_on_bg_or_bap("https://webhook.site/b8c0ef18-f162-417b-95bf-3d62352f271b/search",
                      search_payload_or_select_response1)
    search_message_id1 = search_payload_or_select_response1[constant.CONTEXT]['message_id']
    make_logistics_search_request(search_payload_or_select_response1)
