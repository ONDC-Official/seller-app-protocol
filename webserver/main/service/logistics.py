from main.logger.custom_logging import log
from main.models import get_mongo_collection
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository import mongo
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
    collection = get_mongo_collection(request_type.value)
    query_object = {"context.message_id": message_id}
    request_payload = mongo.collection_find_one(collection, query_object)
    bap_endpoint = fetch_gateway_url_from_lookup(domain=request_payload['context']['action'])
    status_code = make_request_over_ondc_network(request_payload, bap_endpoint, request_type.value)
    log(f"Sent request to logistics-bg with status-code {status_code}")


if __name__ == "__main__":
    pass
