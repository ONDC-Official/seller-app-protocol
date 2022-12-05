from main.logger.custom_logging import log
from main.utils.cryptic_utils import create_authorisation_header
from main.utils.webhook_utils import post_on_bg_or_bap


def make_request_over_ondc_network(payload, end_point, action):
    log(f"Making request over ondc network on {end_point} with action {action}")
    url_with_route = f"{end_point}{action}" \
        if end_point.endswith("/") \
        else f"{end_point}/{action}"
    auth_header = create_authorisation_header(payload)
    status_code = post_on_bg_or_bap(url_with_route, payload, headers={'Authorization': auth_header})
    return status_code
