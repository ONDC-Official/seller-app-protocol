from main import constant
from main.logger.custom_logging import log
from main.models.ondc_request import OndcAction
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup


def make_logistics_payload_request_to_client(payload, request_type: OndcAction):
    if payload[constant.CONTEXT]["core_version"] != "1.2.0":
        if "issue" in request_type.value:
            return get_responses_from_client(f"client/logistics/{request_type.value}", payload)
        return get_responses_from_client(f"v1/client/logistics/{request_type.value}", payload)
    else:
        return get_responses_from_client(f"v2/client/logistics/{request_type.value}", payload)


@check_for_exception
def send_logistics_payload_to_client(payload, request_type: OndcAction):
    log(f"logistics payload to internal client: {payload}")
    resp, return_code = make_logistics_payload_request_to_client(payload, request_type)
    log(f"Got response {resp} from client with status-code {return_code}")
    return resp, return_code


@check_for_exception
def make_logistics_request(request_payload, request_type: OndcAction):
    log(f"logistic request payload to network: {request_payload}")
    if request_payload['context']['action'] == "search":
        endpoint = fetch_gateway_url_from_lookup(domain=request_payload['context']['domain'])
    else:
        endpoint = request_payload['context']['bpp_uri']
    resp, status_code = make_request_over_ondc_network(request_payload, endpoint, request_type.value)
    log(f"Sent request to logistics-bg with status-code {status_code}")
    return resp, status_code


if __name__ == "__main__":
    pass
