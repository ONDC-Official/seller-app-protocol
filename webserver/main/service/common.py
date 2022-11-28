import json
import requests

from main.config import get_config_by_name
from main.logger.custom_logging import log
from main.models.error import DatabaseError
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.ack_response import get_ack_response
from main.repository.db import add_ondc_request, get_first_ondc_request
from main.service.utils import make_request_over_ondc_network
from main.utils.cryptic_utils import create_authorisation_header
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap


@check_for_exception
def send_bpp_responses_to_bg_or_bpp(message):
    request_type = message['request_type']
    log(f"{request_type} payload: {message}")
    message_id = message['message_ids'][request_type]
    payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction(request_type), message_id)
    client_responses, _ = get_responses_from_client(request_type, payload)

    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup() if request_type == "search" else \
        payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(client_responses, gateway_or_bap_endpoint,
                                                 client_responses['context']['action'])
    # status_code = requests.post(f"https://webhook.site/895b3178-368d-4347-9cb6-a4512a1dd73e/{request_type}",
    #                             json=payload, headers={'Authorization': auth_header})
    log(f"Sent responses to bg/bap with status-code {status_code}")


def get_responses_from_client(request_type, payload):
    client_endpoint = get_config_by_name('BPP_CLIENT_ENDPOINT')
    response = requests.post(f"{client_endpoint}/{request_type}", json=payload)
    return json.loads(response.text), response.status_code


def dump_request_payload(request_payload, domain):
    message_id = request_payload['context']['message_id']
    action = request_payload['context']['action']
    is_successful = add_ondc_request(domain=OndcDomain(domain), action=OndcAction(action), message_id=message_id,
                                        request=request_payload)
    if is_successful:
        return get_ack_response(ack=True)
    else:
        return get_ack_response(ack=False, error=DatabaseError.ON_WRITE_ERROR.value)
