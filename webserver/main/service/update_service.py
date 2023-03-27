from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_update_request(payload):
    bpp_endpoint = payload['context']['bpp_uri']
    status_code = make_request_over_ondc_network(payload, bpp_endpoint, payload['context']['action'])
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_retail_update_payload_request_to_client(update_payload):
    return get_responses_from_client("client/update", update_payload)


@check_for_exception
def send_update_payload_to_client(message):
    log(f"retail update payload: {message}")
    update_message_id = message['message_ids']['update']
    update_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('update'), update_message_id)
    resp, return_code = make_retail_update_payload_request_to_client(update_payload)
    log(f"Got response {resp} from client with status-code {return_code}")


@check_for_exception
def make_logistics_update(message):
    log(f"logistics update payload: {message}")
    update_message_id = message['message_ids']['update']
    update_payload = get_first_ondc_request(OndcDomain.LOGISTICS, OndcAction('update'), update_message_id)
    update_payload['context']['bap_uri'] = f"{update_payload['context']['bap_uri']}/protocol/logistics/v1"
    make_logistics_update_request(update_payload)


@check_for_exception
def send_update_response_to_bap(message):
    log(f"retail on_update payload: {message}")
    on_update_message_id = message['message_ids']['on_update']
    on_update_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_update'), on_update_message_id)
    bap_endpoint = on_update_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_update_payload, bap_endpoint, 'on_update')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    pass
