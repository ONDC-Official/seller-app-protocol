import json

from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_init_request(payload):
    bpp_endpoint = payload['context']['bpp_uri']
    status_code = make_request_over_ondc_network(payload, bpp_endpoint, payload['context']['action'])
    log(f"Sent request to logistics-bg/bpp with status-code {status_code}")


def make_retail_init_payload_request_to_client(init_payload):
    return get_responses_from_client("client/init", init_payload)


@check_for_exception
def send_init_payload_to_client(message):
    log(f"retail init payload: {message}")
    init_message_id = message['message_ids']['init']
    init_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('init'), init_message_id)
    resp, return_code = make_retail_init_payload_request_to_client(init_payload)
    log(f"Got response {resp} from client with status-code {return_code}")


@check_for_exception
def make_logistics_init(message):
    log(f"logistics init payload: {message}")
    init_message_id = message['message_ids']['init']
    init_payload = get_first_ondc_request(OndcDomain.LOGISTICS, OndcAction('init'), init_message_id)
    init_payload['context']['bap_uri'] = f"{init_payload['context']['bap_uri']}/protocol/logistics/v1"
    make_logistics_init_request(init_payload)


@check_for_exception
def send_init_response_to_bap(message):
    log(f"retail on_init payload: {message}")
    on_init_message_id = message['message_ids']['on_init']
    on_init_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_init'), on_init_message_id)
    bap_endpoint = on_init_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_init_payload, bap_endpoint, 'on_init')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    pass
