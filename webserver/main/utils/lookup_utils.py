import os

from main.config import get_config_by_name
from main.utils.cryptic_utils import get_filter_dictionary_or_operation, format_registry_request
from main.utils.webhook_utils import lookup_call


def fetch_gateway_url_from_lookup(domain=None):
    if get_config_by_name("BG_DEFAULT_URL_FLAG"):
        return get_config_by_name("BG_DEFAULT_URL")
    else:
        subscriber_type = "BG"
        domain = domain if domain else get_config_by_name('DOMAIN')
        payload = {"type": subscriber_type, "country": get_config_by_name('COUNTRY_CODE'),
                   "domain": domain}
        updated_payload = format_registry_request(payload) if os.getenv("ENV") == "pre_prod" else payload
        response, status_code = lookup_call(f"{get_config_by_name('REGISTRY_BASE_URL')}/lookup",
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


def get_bap_public_key_from_header(auth_header, domain):
    header_parts = get_filter_dictionary_or_operation(auth_header.replace("Signature ", ""))
    subscriber_type = "BAP"
    payload = {"type": subscriber_type, "domain": domain,
               "subscriber_id": header_parts['keyId'].split("|")[0]}
    response, status_code = lookup_call(f"{get_config_by_name('REGISTRY_BASE_URL')}/lookup", payload=payload)
    if status_code == 200:
        return response[0]['signing_public_key']
    else:
        return None


# BPP_PRIVATE_KEY=SHwCJJJoMwrCOmA83ftKBII2YvNB/IJOcAUY3P6Mro4E5Rnks1873hvTn63B4vMTHr9lH+Ia3BMW9b/cE5gh0w==;BPP_PUBLIC_KEY=BOUZ5LNfO94b05+tweLzEx6/ZR/iGtwTFvW/3BOYIdM=;BPP_ID=ref-app-seller-staging-v2.ondc.org;BPP_UNIQUE_KEY_ID=280f8e2a-6f6f-4cb0-868a-2157014f43f5;BPP_URI=https://ref-app-seller-staging-v2.ondc.org