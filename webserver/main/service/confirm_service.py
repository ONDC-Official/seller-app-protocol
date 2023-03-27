import json

from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client, dump_request_payload
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_confirm_request(payload):
    bpp_endpoint = payload['context']['bpp_uri']
    status_code = make_request_over_ondc_network(payload, bpp_endpoint, "confirm")
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_retail_confirm_payload_request_to_client(confirm_payload):
    return get_responses_from_client("client/confirm", confirm_payload)


@check_for_exception
def send_confirm_payload_to_client(message):
    log(f"retail confirm payload: {message}")
    confirm_message_id = message['message_ids']['confirm']
    confirm_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('confirm'), confirm_message_id)
    resp, return_code = make_retail_confirm_payload_request_to_client(confirm_payload)
    log(f"Got response {resp} from client with status-code {return_code}")


@check_for_exception
def make_logistics_confirm(message):
    log(f"logistics confirm payload: {message}")
    confirm_message_id = message['message_ids']['confirm']
    confirm_payload = get_first_ondc_request(OndcDomain.LOGISTICS, OndcAction('confirm'), confirm_message_id)
    confirm_payload['context']['bap_uri'] = f"{confirm_payload['context']['bap_uri']}/protocol/logistics/v1"
    make_logistics_confirm_request(confirm_payload)


@check_for_exception
def send_confirm_response_to_bap(message):
    log(f"retail on_confirm payload: {message}")
    on_confirm_message_id = message['message_ids']['on_confirm']
    on_confirm_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_confirm'), on_confirm_message_id)
    bap_endpoint = on_confirm_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_confirm_payload, bap_endpoint, 'on_confirm')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    pass
