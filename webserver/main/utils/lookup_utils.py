import os

from main.config import get_config_by_name
from main.utils.cryptic_utils import get_filter_dictionary_or_operation, format_registry_request
from main.utils.webhook_utils import lookup_call


def fetch_gateway_url_from_lookup():
    if get_config_by_name("BG_DEFAULT_URL_FLAG"):
        return get_config_by_name("BG_DEFAULT_URL")
    else:
        subscriber_type = "BG"
        payload = {"type": subscriber_type, "country": get_config_by_name('COUNTRY_CODE'),
                   "domain": get_config_by_name('DOMAIN')}
        updated_payload = format_registry_request(payload) if os.getenv("ENV") == "pre_prod" else payload
        lookup_route = "/vlookup" if os.getenv("ENV") == "pre_prod" else "/lookup"
        response, status_code = lookup_call(f"{get_config_by_name('REGISTRY_BASE_URL')}/{lookup_route}",
                                            payload=updated_payload)
        if status_code == 200:
            if response[0].get('network_participant'):
                subscriber_id = response[0]['subscriber_id']
                subscriber_url = response[0].get('network_participant')[0]['subscriber_url']
                return f"https://{subscriber_id}{subscriber_url}"
            else:
                return response[0]['subscriber_url']
        else:
            return None


def get_bap_public_key_from_header(auth_header):
    header_parts = get_filter_dictionary_or_operation(auth_header.replace("Signature ", ""))
    subscriber_type = "BAP"
    payload = {"type": subscriber_type, "domain": get_config_by_name('DOMAIN'),
               "subscriber_id": header_parts['keyId'].split("|")[0]}
    response, status_code = lookup_call(f"{get_config_by_name('REGISTRY_BASE_URL')}/lookup", payload=payload)
    if status_code == 200:
        return response[0]['signing_public_key']
    else:
        return None
