from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request, get_ondc_requests
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_search_request(payload):
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup()
    status_code = make_request_over_ondc_network(payload, gateway_or_bap_endpoint, payload['context']['action'])
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_logistics_search_payload_request_to_client(select_payload):
    return get_responses_from_client("logistics/search-payload-for-retail-select", select_payload)


def make_retail_select_payload_request_to_client(select_payload):
    return get_responses_from_client("client/select", select_payload)


@check_for_exception
def make_logistics_search_or_send_bpp_failure_response(message):
    log(f"retail select payload: {message}")
    select_message_id = message['message_ids']['select']
    select_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('select'), select_message_id)
    search_payloads_or_on_select, return_code = make_logistics_search_payload_request_to_client(select_payload)
    if return_code == 200:
        for p in search_payloads_or_on_select:
            p['context']['bap_uri'] = f"{p['context']['bap_uri']}/protocol/logistics/v1"
            make_logistics_search_request(p)
    else:
        bap_endpoint = select_payload['context']['bap_uri']
        # url_with_route = f"{bap_endpoint}on_select" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_select"
        # send_on_select_to_bap(url_with_route, search_payload_or_select_response)
        status_code = make_request_over_ondc_network(search_payloads_or_on_select, bap_endpoint, 'on_select')
        log(f"Sent responses to bg/bap with status-code {status_code}")


@check_for_exception
def send_select_payload_to_client(message):
    log(f"retail select payload: {message}")
    select_message_id = message['message_ids']['select']
    select_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('select'), select_message_id)
    resp, return_code = make_retail_select_payload_request_to_client(select_payload)
    log(f"Got response {resp} from client with status-code {return_code}")


@check_for_exception
def make_logistics_search(message):
    log(f"logistics search payload: {message}")
    search_message_id = message['message_ids']['search']
    search_payload = get_first_ondc_request(OndcDomain.LOGISTICS, OndcAction('search'), search_message_id)
    search_payload['context']['bap_uri'] = f"{search_payload['context']['bap_uri']}/protocol/logistics/v1"
    make_logistics_search_request(search_payload)


@check_for_exception
def send_select_response_to_bap(message):
    log(f"retail on_select payload: {message}")
    on_select_message_id = message['message_ids']['on_select']
    on_select_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_select'), on_select_message_id)
    bap_endpoint = on_select_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_select_payload, bap_endpoint, 'on_select')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    search_payloads_or_select1, status_code1 = make_logistics_search_payload_request_to_client({})
    post_on_bg_or_bap("https://webhook.site/b8c0ef18-f162-417b-95bf-3d62352f271b/search",
                      search_payloads_or_select1)
    # search_message_id1 = search_payload_or_select_response1[constant.CONTEXT]['message_id']
    [make_logistics_search_request(p) for p in search_payloads_or_select1]
