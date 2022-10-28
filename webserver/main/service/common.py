import json
import requests

from main.config import get_config_by_name
from main.logger.custom_logging import log
from main.models import get_mongo_collection
from main.models.error import DatabaseError
from main.repository import mongo
from main.repository.ack_response import get_ack_response
from main.utils.cryptic_utils import create_authorisation_header
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap

# rabbitmq_connection, rabbitmq_channel = None, None
#
#
# @retry(StreamLostError, tries=3, delay=1, jitter=(1, 3))
# def send_message_to_queue_for_given_request(request_type, payload):
#     global rabbitmq_connection, rabbitmq_channel
#     rabbitmq_connection, rabbitmq_channel = open_connection_and_channel_if_not_already_open(rabbitmq_connection,
#                                                                                             rabbitmq_channel)
#     queue_name = get_config_by_name('RABBITMQ_QUEUE_NAME')
#     declare_queue(rabbitmq_channel, queue_name)
#     payload['request_type'] = request_type
#     publish_message_to_queue(rabbitmq_channel, exchange='', routing_key=queue_name, body=json.dumps(payload))


@check_for_exception
def send_bpp_responses_to_bg_or_bpp(message):
    request_type = message['request_type']
    log(f"{request_type} payload: {message}")
    message_id = message['message_ids'][request_type]
    mongo_collection = get_mongo_collection(request_type)
    payload = mongo.collection_find_one(mongo_collection, {"context.message_id": message_id})
    client_responses = get_responses_from_client(request_type, payload)
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup() if request_type == "search" else \
        payload['context']['bap_uri']
    url_with_route = f"{gateway_or_bap_endpoint}{client_responses['context']['action']}" \
        if gateway_or_bap_endpoint.endswith("/") \
        else f"{gateway_or_bap_endpoint}/{client_responses['context']['action']}"

    auth_header = create_authorisation_header(client_responses)
    status_code = post_on_bg_or_bap(url_with_route, client_responses, headers={'Authorization': auth_header})
    # status_code = requests.post(f"https://webhook.site/895b3178-368d-4347-9cb6-a4512a1dd73e/{request_type}",
    #                             json=payload, headers={'Authorization': auth_header})
    log(f"Sent responses to bg/bap with status-code {status_code}")


def get_responses_from_client(request_type, payload):
    client_endpoint = get_config_by_name('BPP_CLIENT_ENDPOINT')
    response = requests.post(f"{client_endpoint}/{request_type}", json=payload)
    return json.loads(response.text)


def dump_request_payload(request_payload, request_type):
    collection_name = get_mongo_collection(request_type)
    is_successful = mongo.collection_insert_one(collection_name, request_payload)
    if is_successful:
        return get_ack_response(ack=True)
    else:
        return get_ack_response(ack=False, error=DatabaseError.ON_WRITE_ERROR.value)
