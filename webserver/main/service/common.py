import json
import requests

from main.config import get_config_by_name
from main.logger.custom_logging import log
from main.utils.webhook_utils import post_on_bg_or_bap
from main.utils.rabbitmq_utils import create_channel, declare_queue, publish_message_to_queue

channel = create_channel()
declare_queue(channel, 'bpp_protocol')


def send_message_to_queue_for_given_request(request_type, payload):
    payload['request_type'] = request_type
    publish_message_to_queue(channel, exchange='', routing_key='bpp_protocol', body=json.dumps(payload))


def send_bpp_responses_to_bg_or_bpp(request_type, payload):
    # search_responses = {
    #     "context": {
    #         "transaction_id": "4c72de11-59e4-4af6-b02a-f0f14d4f0323",
    #         "country": "IND",
    #         "bpp_id": "stagingapigateway.bizom.in/ondc",
    #         "city": "std:080",
    #         "message_id": "e1ce26c7-4f30-4725-92d6-a0056f2fe1bc",
    #         "core_version": "1.0.0",
    #         "ttl": "PT1D",
    #         "bap_id": "buyer-app-preprod.ondc.org",
    #         "domain": "nic2004:52110",
    #         "bpp_uri": "https://stagingapigateway.bizom.in/ondc",
    #         "action": "on_select",
    #         "bap_uri": "https://bc6e-103-115-201-43.in.ngrok.io/protocol/v1",
    #         "timestamp": "2022-08-18T05:27:47.143Z"
    #     },
    #     "message": {}
    # }
    # status_code = post_on_bg_or_bap(f"https://webhook.site/895b3178-368d-4347-9cb6-a4512a1dd73e/{search_responses['context']['action']}", search_responses)
    client_responses = get_responses_from_client(request_type, payload)
    status_code = post_on_bg_or_bap(f"{payload['context']['bap_uri']}/{client_responses['context']['action']}",
                                    client_responses)
    log(f"Sent responses to bg/bap with status-code {status_code}")


def get_responses_from_client(request_type, payload):
    client_endpoint = get_config_by_name('BPP_CLIENT_ENDPOINT')
    response = requests.post(f"{client_endpoint}/{request_type}", json=payload)
    return json.loads(response.text)

