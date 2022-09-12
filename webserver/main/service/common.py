import json
import requests

from main.config import get_config_by_name
from main.logger.custom_logging import log
from main.utils.webhook_utils import post_on_bg_or_bap
from main.utils.rabbitmq_utils import create_channel, declare_queue, publish_message_to_queue

channel = create_channel()
queue_name = get_config_by_name('RABBITMQ_QUEUE_NAME')
declare_queue(channel, queue_name)


def send_message_to_queue_for_given_request(request_type, payload):
    payload['request_type'] = request_type
    publish_message_to_queue(channel, exchange='', routing_key=queue_name, body=json.dumps(payload))


def send_bpp_responses_to_bg_or_bpp(request_type, payload):
    client_responses = get_responses_from_client(request_type, payload)
    # log(f"Client responses {client_responses}")
    status_code = post_on_bg_or_bap(f"{payload['context']['bap_uri']}/{client_responses['context']['action']}",
                                    client_responses)
    # status_code = requests.post(f"https://webhook.site/895b3178-368d-4347-9cb6-a4512a1dd73e/{request_type}", json=payload)
    log(f"Sent responses to bg/bap with status-code {status_code}")


def get_responses_from_client(request_type, payload):
    client_endpoint = get_config_by_name('BPP_CLIENT_ENDPOINT')
    response = requests.post(f"{client_endpoint}/{request_type}", json=payload)
    return json.loads(response.text)

