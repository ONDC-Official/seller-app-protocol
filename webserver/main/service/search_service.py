from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup


def make_retail_search_payload_request_to_client(search_payload):
    return get_responses_from_client("client/search", search_payload)


@check_for_exception
def send_search_payload_to_client(message):
    log(f"retail search payload: {message}")
    search_message_id = message['message_ids']['search']
    search_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('search'), search_message_id)
    resp, return_code = make_retail_search_payload_request_to_client(search_payload)
    log(f"Got response {resp} from client with status-code {return_code}")


@check_for_exception
def send_search_response_to_gateway(message):
    log(f"retail on_search payload: {message}")
    on_search_message_id = message['message_ids']['on_search']
    on_search_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_search'), on_search_message_id)
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup()
    status_code = make_request_over_ondc_network(on_search_payload, gateway_or_bap_endpoint, 'on_search')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    pass
