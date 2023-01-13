from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_support_request(payload):
    bpp_endpoint = payload['context']['bpp_uri']
    status_code = make_request_over_ondc_network(payload, bpp_endpoint, payload['context']['action'])
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_retail_support_payload_request_to_client(support_payload):
    return get_responses_from_client("client/support", support_payload)


@check_for_exception
def send_support_payload_to_client(message):
    log(f"retail support payload: {message}")
    support_message_id = message['message_ids']['support']
    support_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('support'), support_message_id)
    resp, return_code = make_retail_support_payload_request_to_client(support_payload)
    log(f"Got response {resp} from client with status-code {return_code}")


@check_for_exception
def make_logistics_support(message):
    log(f"logistics support payload: {message}")
    support_message_id = message['message_ids']['support']
    support_payload = get_first_ondc_request(OndcDomain.LOGISTICS, OndcAction('support'), support_message_id)
    support_payload['context']['bap_uri'] = f"{support_payload['context']['bap_uri']}/protocol/logistics/v1"
    make_logistics_support_request(support_payload)


@check_for_exception
def send_support_response_to_bap(message):
    log(f"retail on_support payload: {message}")
    on_support_message_id = message['message_ids']['on_support']
    on_support_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_support'), on_support_message_id)
    bap_endpoint = on_support_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_support_payload, bap_endpoint, 'on_support')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    pass
