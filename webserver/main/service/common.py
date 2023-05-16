import json
import requests

from main.config import get_config_by_name
from main.logger.custom_logging import log
from main.models.error import DatabaseError
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.ack_response import get_ack_response
from main.repository.db import add_ondc_request, get_first_ondc_request, get_ondc_requests
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_count_response_to_client


@check_for_exception
def send_bpp_responses_to_bg_or_bpp(message):
    log(f"{message['request_type']} payload: {message}")
    action = message['request_type'].split("_")[-1]
    message_id = message['message_ids'][action]
    payload = get_first_ondc_request(
        OndcDomain.RETAIL, OndcAction(action), message_id)
    client_responses, _ = get_responses_from_client(action, payload)

    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup() if action == "search" else \
        payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(client_responses, gateway_or_bap_endpoint,
                                                 client_responses['context']['action'])
    # status_code = requests.post(f"https://webhook.site/895b3178-368d-4347-9cb6-a4512a1dd73e/{request_type}",
    #                             json=payload, headers={'Authorization': auth_header})
    log(f"Sent responses to bg/bap with status-code {status_code}")


def get_responses_from_client(request_type, payload):
    if "issue" in request_type:
        client_endpoint = get_config_by_name('IGM_CLIENT_ENDPOINT')
    else:
        client_endpoint = get_config_by_name('BPP_CLIENT_ENDPOINT')
    response = requests.post(f"{client_endpoint}/{request_type}", json=payload)
    return json.loads(response.text), response.status_code


def dump_request_payload(request_payload, domain, action=None):
    message_id = request_payload['context']['message_id']
    action = action if action else request_payload['context']['action']
    is_successful = add_ondc_request(domain=OndcDomain(domain), action=OndcAction(action), message_id=message_id,
                                     request=request_payload)
    if is_successful:
        return get_ack_response(ack=True)
    else:
        return get_ack_response(ack=False, error=DatabaseError.ON_WRITE_ERROR.value)


def get_network_request_payloads(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    response = {}
    for k, v in kwargs.items():
        key_parts = k.split("_", maxsplit=1)
        domain, action = key_parts[0], key_parts[1]
        message_ids = [x.strip() for x in v.split(",")]
        ondc_requests = []
        for m in message_ids:
            ondc_requests.extend(get_ondc_requests(
                OndcDomain(domain), OndcAction(action), m))
        response[k] = ondc_requests
    return response


@check_for_exception
def send_logistics_on_call_count_to_client(message, request_type="on_search"):
    log(f"logistics {request_type} payload: {message}")
    on_call_message_id = message['message_ids'][request_type]
    on_call_requests = get_ondc_requests(
        OndcDomain.LOGISTICS, OndcAction(request_type), on_call_message_id)
    on_call_requests_count = len(on_call_requests)
    on_call_transaction_id = on_call_requests[0]['context'][
        'transaction_id'] if on_call_requests_count > 0 else None
    post_count_response_to_client(request_type,
                                  {
                                      "messageId": on_call_message_id,
                                      "transactionId": on_call_transaction_id,
                                      "count": on_call_requests_count,
                                  })
