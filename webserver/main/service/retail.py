from main import constant
from main.logger.custom_logging import log
from main.models.ondc_request import OndcAction
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception


def make_retail_payload_request_to_client(payload, request_type: OndcAction):
    if payload[constant.CONTEXT]["core_version"] != "1.2.0":
        if "issue" in request_type.value:
            return get_responses_from_client(f"client/{request_type.value}", payload)
        return get_responses_from_client(f"v1/client/{request_type.value}", payload)
    else:
        return get_responses_from_client(f"v2/client/{request_type.value}", payload)


def send_retail_payload_to_client_logistics(payload, request_type: OndcAction):
    log(f"retail payload to logistics internal client: {payload}")
    if payload[constant.CONTEXT]["core_version"] == "1.0.0" and "issue" in request_type.value:
        return get_responses_from_client(f"logistics/{request_type.value}", payload)


@check_for_exception
def send_retail_payload_to_client(payload, request_type: OndcAction):
    log(f"retail payload of {request_type.value} to internal client: {payload}")
    resp, return_code = make_retail_payload_request_to_client(
        payload, request_type)
    log(f"Got response {resp} from client with status-code {return_code}")
    return resp, return_code


@check_for_exception
def send_retail_response_to_ondc_network(request_payload, request_type: OndcAction, headers={}):
    if request_payload["context"]["action"] != "on_search":
        log(f"retail callback payload: {request_payload}")
    bap_endpoint = request_payload["context"]["bap_uri"]
    resp, status_code = make_request_over_ondc_network(request_payload, bap_endpoint, request_type.value, headers)
    log(f"Sent responses to bg/bap with status-code {status_code}")
    return resp, status_code
