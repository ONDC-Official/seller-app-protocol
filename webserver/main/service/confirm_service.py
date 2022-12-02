from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_confirm_request(payload):
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup()
    status_code = make_request_over_ondc_network(payload, gateway_or_bap_endpoint, payload['context']['action'])
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_logistics_confirm_payload_request_to_client(confirm_payload):
    return get_responses_from_client("logistics/confirm-payload-for-retail-confirm", confirm_payload)


@check_for_exception
def make_logistics_confirm_or_send_bpp_failure_response(message):
    log(f"retail confirm payload: {message}")
    confirm_message_id = message['message_ids']['confirm']
    confirm_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('confirm'), confirm_message_id)
    logistics_confirm_payloads_or_on_confirm, return_code = make_logistics_confirm_payload_request_to_client(confirm_payload)
    if return_code == 200:
        for p in logistics_confirm_payloads_or_on_confirm:
            make_logistics_confirm_request(p)
    else:
        bap_endpoint = confirm_payload['context']['bap_uri']
        # url_with_route = f"{bap_endpoint}on_confirm" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_confirm"
        # send_on_confirm_to_bap(url_with_route, search_payload_or_confirm_response)
        status_code = make_request_over_ondc_network(logistics_confirm_payloads_or_on_confirm, bap_endpoint, 'on_confirm')
        log(f"Sent responses to bg/bap with status-code {status_code}")


@check_for_exception
def send_confirm_response_to_bap(message):
    log(f"retail on_confirm payload: {message}")
    on_confirm_message_id = message['message_ids']['on_confirm']
    on_confirm_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_confirm'), on_confirm_message_id)
    bap_endpoint = on_confirm_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_confirm_payload, bap_endpoint, 'on_confirm')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    search_payloads_or_confirm1, status_code1 = make_logistics_confirm_payload_request_to_client({})
    post_on_bg_or_bap("https://webhook.site/b8c0ef18-f162-417b-95bf-3d62352f271b/search",
                      search_payloads_or_confirm1)
    # search_message_id1 = search_payload_or_confirm_response1[constant.CONTEXT]['message_id']
    [make_logistics_confirm_request(p) for p in search_payloads_or_confirm1]
