from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request, get_ondc_requests
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_status_request(payload):
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup()
    status_code = make_request_over_ondc_network(payload, gateway_or_bap_endpoint, payload['context']['action'])
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_logistics_status_payload_request_to_client(status_payload):
    return get_responses_from_client("logistics/search-payload-for-retail-status", status_payload)


@check_for_exception
def make_logistics_status_or_send_bpp_failure_response(message):
    log(f"retail status payload: {message}")
    status_message_id = message['message_ids']['status']
    status_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('status'), status_message_id)
    logistics_status_payloads_or_on_status, return_code = make_logistics_status_payload_request_to_client(status_payload)
    if return_code == 200:
        for p in logistics_status_payloads_or_on_status:
            p['context']['bap_uri'] = f"{p['context']['bap_uri']}/protocol/logistics/v1"
            make_logistics_status_request(p)
    else:
        bap_endpoint = status_payload['context']['bap_uri']
        # url_with_route = f"{bap_endpoint}on_status" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_status"
        # send_on_status_to_bap(url_with_route, search_payload_or_status_response)
        status_code = make_request_over_ondc_network(logistics_status_payloads_or_on_status, bap_endpoint, 'on_status')
        log(f"Sent responses to bg/bap with status-code {status_code}")


@check_for_exception
def send_status_response_to_bap(message):
    log(f"retail on_status payload: {message}")
    on_status_message_id = message['message_ids']['on_status']
    on_status_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_status'), on_status_message_id)
    bap_endpoint = on_status_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_status_payload, bap_endpoint, 'on_status')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    logistics_status_payloads_or_status1, status_code1 = make_logistics_status_payload_request_to_client({})
    post_on_bg_or_bap("https://webhook.site/b8c0ef18-f162-417b-95bf-3d62352f271b/search",
                      logistics_status_payloads_or_status1)
    # search_message_id1 = search_payload_or_status_response1[constant.CONTEXT]['message_id']
    [make_logistics_status_request(p) for p in logistics_status_payloads_or_status1]
