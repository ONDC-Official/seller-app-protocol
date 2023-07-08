from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup


def make_logistics_request_payload_request_to_client(payload, retail_type: OndcAction, logistics_type: OndcAction):
    return get_responses_from_client(f"logistics/{logistics_type.value}-payload-for-retail-{retail_type.value}",
                                     payload)


@check_for_exception
def make_logistics_request(message, request_type: OndcAction):
    log(f"logistics payload: {message}")
    message_id = message['message_ids'][request_type.value]
    payload = get_first_ondc_request(OndcDomain.LOGISTICS, request_type, message_id)
    payload['context']['bap_uri'] = f"{payload['context']['bap_uri']}/protocol/logistics/v1"
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup()
    status_code = make_request_over_ondc_network(payload, gateway_or_bap_endpoint, payload['context']['action'])
    log(f"Sent request to logistics-bg with status-code {status_code}")


if __name__ == "__main__":
    pass
