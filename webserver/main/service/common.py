import json
from datetime import datetime

import requests

from main.config import get_config_by_name
from main.logger.custom_logging import log
from main.models import get_mongo_collection
from main.models.error import DatabaseError
from main.models.ondc_request import OndcDomain, OndcAction, OndcRequest
from main.repository import mongo
from main.repository.ack_response import get_ack_response
from main.repository.db import get_ondc_requests
from main.utils.decorators import check_for_exception
from main.utils.webhook_utils import post_count_response_to_client


def get_responses_from_client(request_type, payload):
    if "issue" in request_type:
        client_endpoint = get_config_by_name('IGM_CLIENT_ENDPOINT')
    else:
        client_endpoint = get_config_by_name('BPP_CLIENT_ENDPOINT')
    response = requests.post(f"{client_endpoint}/{request_type}", json=payload)
    return json.loads(response.text) if response.status_code == 200 else None, response.status_code


def dump_request_payload(request_payload, domain, action=None):
    action = action if action else request_payload['context']['action']
    collection_name = get_mongo_collection(action)
    filter_criteria = {"context.message_id": request_payload['context']['message_id']}
    if domain == OndcDomain.LOGISTICS.value:
        filter_criteria["context.bpp_id"] = request_payload['context']['bpp_id']
    request_payload['created_at'] = datetime.utcnow()
    update_data = {'$set': request_payload}
    is_successful = mongo.collection_upsert_one(collection_name, filter_criteria, update_data)
    request_payload.pop('created_at')
    if is_successful:
        return get_ack_response(context=request_payload['context'], ack=True)
    else:
        return get_ack_response(context=request_payload['context'], ack=False, error=DatabaseError.ON_WRITE_ERROR.value)


def get_network_request_payloads(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    response = {}
    for k, v in kwargs.items():
        key_parts = k.split("_", maxsplit=1)
        domain, action = key_parts[0], key_parts[1]
        message_ids = [x.strip() for x in v.split(",")]
        search_collection = get_mongo_collection(action)
        query_object = {"context.message_id": {"$in": message_ids}}
        catalogs = mongo.collection_find_all(
            search_collection, query_object)["data"]
        response[k] = catalogs
    return response


def get_active_ondc_requests():
    search_collection = get_mongo_collection("search")
    query_object = {"message.intent.tags.code": "catalog_inc"}
    catalogs = mongo.collection_find_all(search_collection, query_object)
    return catalogs


@check_for_exception
def send_logistics_on_call_count_to_client(request_payload, request_type="on_search"):
    on_call_message_id = request_payload['context']['message_id']
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
