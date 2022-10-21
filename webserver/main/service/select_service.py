import json
import time

import pika

from main import constant
from main.config import get_config_by_name
from main.logger.custom_logging import log
from main.models import get_mongo_collection
from main.repository import mongo
from main.service import send_message_to_queue_for_given_request
from main.utils.cryptic_utils import create_authorisation_header
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap

rabbitmq_connection, rabbitmq_channel = None, None


def make_logistics_search_request(payload):
    gateway_or_bap_endpoint = fetch_gateway_url_from_lookup()
    url_with_route = f"{gateway_or_bap_endpoint}{payload['context']['action']}" \
        if gateway_or_bap_endpoint.endswith("/") \
        else f"{gateway_or_bap_endpoint}/{payload['context']['action']}"
    auth_header = create_authorisation_header(payload)
    status_code = post_on_bg_or_bap(url_with_route, payload, headers={'Authorization': auth_header})
    print(status_code)


def make_select_request_to_client(select_payload):
    return 200, json.loads('''
        {
    "context": {
        "action": "on_select",
        "bap_id": "ondc.paytm.com",
        "bap_uri": "https://ondc.paytm.com/retail",
        "bpp_id": "ondc.gofrugal.com/ondc/18275",
        "bpp_uri": "https://ondc.gofrugal.com/ondc/seller/adaptor",
        "city": "std:080",
        "core_version": "1.0.0",
        "country": "IND",
        "domain": "nic2004:52110",
        "message_id": "1652092268191",
        "timestamp": "2022-05-09T10:31:08.201Z",
        "transaction_id": "9fdb667c-76c6-456a-9742-ba9caa5eb765"
    },
    "message": {
        "order": {
            "fulfillments": [
                {
                    "@ondc/org/category": "Immediate Delivery",
                    "@ondc/org/provider_name": "Loadshare",
                    "@ondc/org/TAT": "PT45M",
                    "id": "Fulfillment1",
                    "state": {
                        "descriptor": {
                            "name": "Serviceable"
                        }
                    },
                    "tracking": false
                }
            ],
            "items": [
                {
                    "fulfillment_id": "Fulfillment1",
                    "id": "18275-ONDC-1-9"
                }
            ],
            "provider": {
                "id": "18275-ONDC-1-11094"
            },
            "quote": {
                "breakup": [
                    {
                        "@ondc/org/item_id": "18275-ONDC-1-9",
                        "@ondc/org/item_quantity": {
                            "count": 1
                        },
                        "@ondc/org/title_type": "item",
                        "item": {
                            "price": {
                                "currency": "INR",
                                "value": "5.0"
                            },
                            "quantity": {
                                "available": {
                                    "count": "1"
                                },
                                "maximum": {
                                    "count": "1"
                                }
                            }
                        },
                        "price": {
                            "currency": "INR",
                            "value": "5.0"
                        },
                        "title": "SENSODYNE SENSITIVE TOOTH BRUSH"
                    },
                    {
                        "@ondc/org/item_id": "Fulfillment1",
                        "@ondc/org/title_type": "delivery",
                        "price": {
                            "currency": "INR",
                            "value": "0.5"
                        },
                        "title": "Delivery charges"
                    },
                    {
                        "@ondc/org/item_id": "Fulfillment1",
                        "@ondc/org/title_type": "packing",
                        "price": {
                            "currency": "INR",
                            "value": "0.5"
                        },
                        "title": "Packing charges"
                    },
                    {
                        "@ondc/org/title_type": "tax",
                        "price": {
                            "currency": "INR",
                            "value": "0.9"
                        },
                        "title": "Tax"
                    }
                ],
                "price": {
                    "currency": "INR",
                    "value": "6.9"
                },
                "ttl": "P1D"
            }
        }
    }
}
        ''')


def make_logistics_search_payload_request_to_client(select_payload):
    return 200, json.loads('''
    {
    "context": {
        "domain": "nic2004:60232",
        "country": "IND",
        "city": "std:080",
        "action": "search",
        "core_version": "1.0.0",
        "bap_id": "sellerapp-staging.datasyndicate.in",
        "bap_uri": "https://85ec-103-115-201-50.in.ngrok.io/protocol/v1",
        "transaction_id": "9fdb667c-76c6-456a-9742-ba9caa5eb765",
        "message_id": "1651742565654",
        "timestamp": "2022-06-13T07:22:45.363Z",
        "ttl": "PT30S"
    },
    "message": {
        "intent": {
            "category": {
                "id": "Immediate Delivery"
            },
            "provider": {
                "time": {
                    "days": "1,2,3,4,5,6,7",
                    "schedule": {
                        "holidays": [
                            "2022-08-15",
                            "2022-08-19"
                        ],
                        "frequency": "PT4H",
                        "times": [
                            "1100",
                            "1900"
                        ]
                    },
                    "range": {
                        "start": "1100",
                        "end": "2100"
                    }
                }
            },
            "fulfillment": {
                "type": "CoD",
                "start": {
                    "location": {
                        "gps": "12.4535445,77.9283792",
                        "address": {
                            "area_code": "560041"
                        }
                    }
                },
                "end": {
                    "location": {
                        "gps": "12.4535445,77.9283792",
                        "address": {
                            "area_code": "560001"
                        }
                    }
                }
            },
            "payment": {
                "@ondc/org/collection_amount": "30000"
            },
            "@ondc/org/payload_details": {
                "weight": {
                    "unit": "Kilogram",
                    "value": 10
                },
                "dimensions": {
                    "length": {
                        "unit": "meter",
                        "value": 1
                    },
                    "breadth": {
                        "unit": "meter",
                        "value": 1
                    },
                    "height": {
                        "unit": "meter",
                        "value": 1
                    }
                },
                "category": "Mobile Phone",
                "value": {
                    "currency": "INR",
                    "value": "50000"
                }
            }
        }
    }
}
    ''')


def send_on_select_to_bap(url_with_route, payload):
    auth_header = create_authorisation_header(payload)
    # status_code = post_on_bg_or_bap(url_with_route, payload, headers={'Authorization': auth_header})
    import requests
    status_code = requests.post(f"https://webhook.site/895b3178-368d-4347-9cb6-a4512a1dd73e/on_select",
                                json=payload, headers={'Authorization': auth_header})
    log(f"Sent responses to bg/bap with status-code {status_code}")


def make_logistics_search_or_send_bpp_failure_response(message):
    log(f"select_1 payload: {message}")
    select_message_id = message['message_ids']['select']
    select_collection = get_mongo_collection('select')
    select_payload = mongo.collection_find_one(select_collection, {"context.message_id": select_message_id})
    return_code, search_payload_or_select_response = make_logistics_search_payload_request_to_client(select_payload)
    if return_code == 200:
        search_message_id = search_payload_or_select_response[constant.CONTEXT]['message_id']
        make_logistics_search_request(search_payload_or_select_response)
        message['request_type'] = "select_2"
        message['message_ids']['logistics_search'] = search_message_id
        send_message_to_queue_for_given_request(message,
                                                properties=pika.BasicProperties(headers={
                                                    "x-delay": get_config_by_name("LOGISTICS_ON_SEARCH_WAIT")*1000,
                                                }))
    else:
        bap_endpoint = select_payload['context']['bap_uri']
        url_with_route = f"{bap_endpoint}on_select" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_select"
        send_on_select_to_bap(url_with_route, search_payload_or_select_response)


def send_select_response_to_bap(message):
    log(f"select_2 payload: {message}")
    select_message_id = message['message_ids']['select']
    logistics_search_message_id = message['message_ids']['logistics_search']
    select_collection = get_mongo_collection('select')
    logistics_search_collection = get_mongo_collection('logistics_on_search')
    payload = {
        "select_payload": mongo.collection_find_one(select_collection, {"context.message_id": select_message_id}),
        "on_search_payload": mongo.collection_find_all(logistics_search_collection,
                                                       {"context.message_id": logistics_search_message_id})
    }
    print(f"final_payload {payload}")
    status_code, select_resp = make_select_request_to_client(payload)

    bap_endpoint = select_resp['context']['bap_uri']
    url_with_route = f"{bap_endpoint}on_select" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_select"
    send_on_select_to_bap(url_with_route, select_resp)


if __name__ == "__main__":
    make_logistics_search_or_send_bpp_failure_response(json.loads('''
    {
"context":
{
"domain": "nic2004:52110",
"action": "select",
"core_version": "1.0.0",
"bap_id": "ondc.paytm.com",
"bap_uri": "https://ondc.paytm.com/retail",
"bpp_id": "ondc.gofrugal.com/ondc/18275",
"bpp_uri": "https://ondc.gofrugal.com/ondc/seller/adaptor",
"transaction_id": "9fdb667c-76c6-456a-9742-ba9caa5eb765",
"message_id": "1652092268191",
"city": "std:080",
"country": "IND",
"timestamp": "2022-05-09T10:31:08.201Z",
"ttl": "PT30S"
},
"message":
{
"order":
{
"provider":
{
"id": "18275-ONDC-1-11094",
"locations":
[
   {

"id": "18275-ONDC-1-11094"
   }
]
},
"items":
[
{
"id": "18275-ONDC-1-9",
"location_id": "abc-store-location-id-1",
"quantity":
{
"count": 1
},
"price":
{
"currency": "INR",
"value": 5.0
}
}
],
"fulfillments":
[
{
               "end":
  {
                   "location" :
      {
                       "gps" : "12.4535445,77.9283792",
	          "address":
	          {
		 "area_code": "560001"
	          			          }
                   	      }
               }
            }
            ]
}
}
}
    '''))