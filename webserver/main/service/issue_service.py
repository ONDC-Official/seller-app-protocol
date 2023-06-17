from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_issue_request(payload):
    bpp_endpoint = payload['context']['bpp_uri']
    status_code = make_request_over_ondc_network(
        payload, bpp_endpoint, payload['context']['action'])
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_retail_issue_payload_request_to_client(issue_payload):
    return get_responses_from_client("client/issue", issue_payload)


@check_for_exception
def send_issue_payload_to_client(message):
    log(f"retail issue payload: {message}")
    issue_message_id = message['message_ids']['issue']
    issue_payload = get_first_ondc_request(
        OndcDomain.RETAIL, OndcAction('issue'), issue_message_id)
    resp, return_code = make_retail_issue_payload_request_to_client(
        issue_payload)
    log(f"Got response {resp} from client with status-code {return_code}")


@check_for_exception
def make_logistics_issue(message):
    log(f"logistics issue payload: {message}")
    issue_message_id = message['message_ids']['issue']
    issue_payload = get_first_ondc_request(
        OndcDomain.LOGISTICS, OndcAction('issue'), issue_message_id)
    issue_payload['context']['bap_uri'] = f"{issue_payload['context']['bap_uri']}/protocol/logistics/v1"
    make_logistics_issue_request(issue_payload)


@check_for_exception
def send_issue_response_to_bap(message):
    log(f"retail on_issue payload: {message}")
    on_issue_message_id = message['message_ids']['on_issue']
    on_issue_payload = get_first_ondc_request(
        OndcDomain.RETAIL, OndcAction('on_issue'), on_issue_message_id)
    bap_endpoint = on_issue_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(
        on_issue_payload, bap_endpoint, 'on_issue')
    log(f"Sent responses to bg/bap with status-code {status_code}")

