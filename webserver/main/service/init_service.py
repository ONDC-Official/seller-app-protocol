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


def make_logistics_init_payload_request_to_client(init_payload):
    return get_responses_from_client("logistics/init-payload-for-retail-init", init_payload)


@check_for_exception
def make_logistics_init_or_send_bpp_failure_response(message):
    log(f"retail init payload: {message}")
    init_message_id = message['message_ids']['init']
    init_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('init'), init_message_id)
    logistics_init_payloads_or_on_init, return_code = make_logistics_init_payload_request_to_client(init_payload)
    if return_code == 200:
        for p in logistics_init_payloads_or_on_init:
            p['context']['bap_uri'] = f"{p['context']['bap_uri']}/protocol/logistics/v1"
            make_logistics_init_request(p)
    else:
        bap_endpoint = init_payload['context']['bap_uri']
        # url_with_route = f"{bap_endpoint}on_init" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_init"
        # send_on_init_to_bap(url_with_route, search_payload_or_init_response)
        status_code = make_request_over_ondc_network(logistics_init_payloads_or_on_init, bap_endpoint, 'on_init')
        log(f"Sent responses to bg/bap with status-code {status_code}")


@check_for_exception
def send_init_response_to_bap(message):
    log(f"retail on_init payload: {message}")
    on_init_message_id = message['message_ids']['on_init']
    on_init_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_init'), on_init_message_id)
    bap_endpoint = on_init_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_init_payload, bap_endpoint, 'on_init')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    search_payloads_or_init1, status_code1 = make_logistics_init_payload_request_to_client({})
    post_on_bg_or_bap("https://webhook.site/b8c0ef18-f162-417b-95bf-3d62352f271b/search",
                      search_payloads_or_init1)
    # search_message_id1 = search_payload_or_init_response1[constant.CONTEXT]['message_id']
    [make_logistics_init_request(p) for p in search_payloads_or_init1]
