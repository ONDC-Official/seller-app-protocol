from main import constant
from main.logger.custom_logging import log
from main.models.ondc_request import OndcAction, OndcDomain
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup


def make_retail_payload_request_to_client(payload, request_type: OndcAction):
    if payload[constant.CONTEXT]["core_version"] != "1.2.0":
        return get_responses_from_client(f"client/v1/{request_type.value}", payload)
    else:
        return get_responses_from_client(f"client/v2/{request_type.value}", payload)


@check_for_exception
def send_retail_payload_to_client(message, request_type: OndcAction):
    log(f"retail payload: {message}")
    search_message_id = message['message_ids'][request_type.value]
    search_payload = get_first_ondc_request(OndcDomain.RETAIL, request_type, search_message_id)
    resp, return_code = make_retail_payload_request_to_client(search_payload, request_type)
    log(f"Got response {resp} from client with status-code {return_code}")


@check_for_exception
def send_retail_response_to_ondc_network(message, request_type: OndcAction):
    log(f"retail callback payload: {message}")
    message_id = message['message_ids'][request_type.value]
    payload = get_first_ondc_request(OndcDomain.RETAIL, request_type, message_id)
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup()
    status_code = make_request_over_ondc_network(payload, gateway_or_bap_endpoint, request_type.value)
    log(f"Sent responses to bg/bap with status-code {status_code}")
