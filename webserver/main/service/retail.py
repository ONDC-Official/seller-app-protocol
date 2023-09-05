from main import constant
from main.logger.custom_logging import log
from main.models import get_mongo_collection
from main.models.ondc_request import OndcAction, OndcDomain
from main.repository import mongo
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup


def make_retail_payload_request_to_client(payload, request_type: OndcAction):
    if payload[constant.CONTEXT]["core_version"] != "1.2.0":
        return get_responses_from_client(f"v1/client/{request_type.value}", payload)
    else:
        return get_responses_from_client(f"v2/client/{request_type.value}", payload)


@check_for_exception
def send_retail_payload_to_client(payload, request_type: OndcAction):
    log(f"retail payload: {payload}")
    resp, return_code = make_retail_payload_request_to_client(payload, request_type)
    log(f"Got response {resp} from client with status-code {return_code}")
    return resp, return_code


@check_for_exception
def send_retail_response_to_ondc_network(message, request_type: OndcAction):
    log(f"retail callback payload: {message}")
    message_id = message['message_ids'][request_type.value]
    collection = get_mongo_collection(request_type.value)
    query_object = {"context.message_id": message_id}
    request_payload = mongo.collection_find_one(collection, query_object)
    bap_endpoint = request_payload["context"]["bap_uri"]
    status_code = make_request_over_ondc_network(request_payload, bap_endpoint, request_type.value)
    log(f"Sent responses to bg/bap with status-code {status_code}")
