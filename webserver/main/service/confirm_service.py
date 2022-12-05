import json

from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.repository.db import get_first_ondc_request
from main.service.common import get_responses_from_client, dump_request_payload
from main.service.utils import make_request_over_ondc_network
from main.utils.decorators import check_for_exception
from main.utils.lookup_utils import fetch_gateway_url_from_lookup
from main.utils.webhook_utils import post_on_bg_or_bap


def make_logistics_confirm_request(payload):
    bpp_endpoint = payload['context']['bpp_uri']
    status_code = make_request_over_ondc_network(payload, bpp_endpoint, "confirm")
    log(f"Sent request to logistics-bg with status-code {status_code}")


def make_logistics_confirm_payload_request_to_client(confirm_payload):
    return get_responses_from_client("logistics/confirm-payload-for-retail-confirm", confirm_payload)


@check_for_exception
def make_logistics_confirm_or_send_bpp_failure_response(message):
    log(f"retail confirm payload: {message}")
    confirm_message_id = message['message_ids']['confirm']
    confirm_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('confirm'), confirm_message_id)
    logistics_confirm_payloads_or_on_confirm, return_code = make_logistics_confirm_payload_request_to_client(confirm_payload)
    if return_code == 200:
        for p in logistics_confirm_payloads_or_on_confirm:
            p['context']['bap_uri'] = f"{p['context']['bap_uri']}/protocol/logistics/v1"
            make_logistics_confirm_request(p)
#             logistics_payload = json.loads('''
#             {
#   "context":
#   {
#       "domain": "nic2004:60232",
#       "country": "IND",
#       "city": "std:080",
#       "action": "on_confirm",
#       "core_version": "1.0.0",
#       "bap_id": "ondc.gofrugal.com/ondc/18275",
#       "bap_uri": "https://ondc.gofrugal.com/ondc/seller/adaptor",
#       "bpp_id": "shiprocket.com/ondc/18275",
#       "bpp_uri": "https://shiprocket.com/ondc",
#       "transaction_id": "9fdb667c-76c6-456a-9742-ba9caa5eb765",
#       "message_id": "1651742565654",
#       "timestamp": "2022-06-13T07:22:45.363Z"
#   },
#   "message":
#   {
#     "order":
#     {
#       "id": "0799f385-5043-4848-8433-4643ad511a14",
#       "state": "Accepted",
#       "provider":
#       {
#         "id": "18275-Provider-1",
#         "locations":
#         [
#           {
#             "id": "18275-Location-1"
#           }
#         ]
#       },
#       "items":
#       [
#         {
#           "id": "18275-Item-1",
#           "category_id": "Same Day Delivery"
#         }
#       ],
#       	      "quote":
#       	      {
#         "price":
#         	        {
#           "currency": "INR",
#          	          "value": "7.0"
#         },
#        	        "breakup":
#         	        [
#           		{
#             	  	"@ondc/org/item_id": "18275-Item-1",
#              "@ondc/org/title_type": "Delivery Charge",
#             			 "price":
#             		  	 {
#               		"currency": "INR",
#              	 	"value": "5.0"
#             			  }
#           		},
#           		{
#             			"title": "RTO charges",
#             "@ondc/org/title_type": "RTO Charge",
#             "price":
#             {
#               "currency": "INR",
#               "value": "2.0"
#             			}
#           		}
#         	        ]
#      	      },
#       "fulfillments":
#       [
#         {
#           "id": "Fulfillment1",
#           "type": "CoD",
#           "state":
#           {
#       "descriptor":
#       {
# 	"code": "Pending",
# 		"name": "Pending"
#       }
#           },
#           "@ondc/org/awb_no": "1227262193237777",
#           "tracking": false,
#           "start":
#           {
#             "time":
#             {
#               "range":
#               {
#                 "start": "2022-06-14T10:00:00.000Z",
#                 "end": "2022-06-14T10:30:00.000Z"
#               }
#             }
#           },
#           "end":
#           {
#             "time":
#             {
#               "range":
#               {
#                 "start": "2022-06-14T12:00:00.000Z",
#                 "end": "2022-06-14T12:30:00.000Z"
#               }
#             }
#           },
#           "agent":
#           {
#             "name": "Ramu",
#             "phone": "9886098860"
#           },
#           "vehicle":
#           {
#             "category": "mini-truck",
#             "size": "small",
#             "registration": "2020"
#           },
#           "@ondc/org/ewaybillno": "EBN1",
#           "@ondc/org/ebnexpirydate": "2022-06-30T12:00:00.000Z"
#         },
#         {
#           "id": "Fulfillment1-RTO",
#           "type": "RTO",
#           "start":
#           {
#             "time":
#             {
#               "range":
#               {
#                 "start": "2022-06-14T10:00:00.000Z",
#                 "end": "2022-06-14T10:30:00.000Z"
#               }
#             }
#           },
#           "agent":
#           {
#             "name": "Ramu",
#             "phone": "9886098860"
#           }
#         }
#       ],
#       "billing":
#       {
#         "name": "XXXX YYYYY",
#         "address":
#         {
#           "name": "D000, Prestige Towers",
#           "locality": "Bannerghatta Road",
#           "city": "Bengaluru",
#           "state": "Karnataka",
#           "country": "India",
#           "area_code": "560076"
#         },
#         "tax_number": "29AAACU1901H1ZK",
#         "phone": "98860 98860",
#         "email": "abcd.efgh@gmail.com"
#       },
#       "cancellation_terms":
#       [
#        {
#          "fulfillment_state":
#          {
#  	"descriptor":
# 	{
# 		"code":"Agent-assigned"
# 	}
#          },
#          "cancellation_fee":
#          {
# 	"percentage":"5",
# 	"amount":
# 	{
# 		"currency":"INR",
# 		"value":"50"
# 	}
#          }
#        },
#        {
#          "fulfillment_state":
#          {
# 	"descriptor":
# 	{
# 		"code":"Order-picked-up"
# 	}
#          },
#          "cancellation_fee":
#          {
# 	"percentage":"25",
# 	"amount":
# 	{
# 		"currency":"INR",
# 		"value":"100"
# 	}
#          }
#        },
#        {
#          "fulfillment_state":
#          {
# 	"descriptor":
# 	{
# 		"code":"Out-for-delivery"
# 	}
#          },
#          "cancellation_fee":
#          {
# 	"percentage":"75",
# 	"amount":
# 	{
# 		"currency":"INR",
# 		"value":"250"
# 	}
#          }
#        }
#      ],
#      "tags":
#      [
#       {
#         "code":"bpp_terms_liability",
#         "list":
#         [
#           {
#             "code":"max_liability_cap",
#             "value":"10000"
#           },
#           {
#             "code":"max_liability",
#             "value":"2"
#           },
#           {
#             "code":"accept",
#             "value":"Y"
#           }
#         ]
#       },
#       {
#         "code":"bpp_terms_arbitration",
#         "list":
#         [
#           {
#             "code":"mandatory_arbitration",
#             "value":"false"
#           },
#           {
#             "code":"court_jurisdiction",
#             "value":"KA"
#           },
#           {
#             "code":"accept",
#             "value":"Y"
#           }
#         ]
#       },
#       {
#         "code":"bpp_terms_charges",
#         "list":
#         [
#           {
#             "code":"delay_interest",
#             "value":"1000"
#           },
#           {
#             "code":"max_delay_charges",
#             "value":"1000"
#           },
#           {
#             "code":"accept",
#             "value":"Y"
#           }
#         ]
#       }
#     ]
#     }
#   }
# }
#             ''')
#             print(f"dumping for msg id: {p['context']['message_id']}")
#             logistics_payload['context']['transaction_id'] = p['context']['transaction_id']
#             logistics_payload['context']['message_id'] = p['context']['message_id']
#             logistics_payload['context']['bpp_id'] = p['context']['bpp_id']
#             logistics_payload['context']['bpp_uri'] = p['context']['bpp_uri']
#             dump_request_payload(logistics_payload, domain=OndcDomain.LOGISTICS.value)
    else:
        bap_endpoint = confirm_payload['context']['bap_uri']
        # url_with_route = f"{bap_endpoint}on_confirm" if bap_endpoint.endswith("/") else f"{bap_endpoint}/on_confirm"
        # send_on_confirm_to_bap(url_with_route, search_payload_or_confirm_response)
        status_code = make_request_over_ondc_network(logistics_confirm_payloads_or_on_confirm, bap_endpoint, 'on_confirm')
        log(f"Sent responses to bg/bap with status-code {status_code}")


@check_for_exception
def send_confirm_response_to_bap(message):
    log(f"retail on_confirm payload: {message}")
    on_confirm_message_id = message['message_ids']['on_confirm']
    on_confirm_payload = get_first_ondc_request(OndcDomain.RETAIL, OndcAction('on_confirm'), on_confirm_message_id)
    bap_endpoint = on_confirm_payload['context']['bap_uri']
    status_code = make_request_over_ondc_network(on_confirm_payload, bap_endpoint, 'on_confirm')
    log(f"Sent responses to bg/bap with status-code {status_code}")


if __name__ == "__main__":
    search_payloads_or_confirm1, status_code1 = make_logistics_confirm_payload_request_to_client({})
    post_on_bg_or_bap("https://webhook.site/b8c0ef18-f162-417b-95bf-3d62352f271b/search",
                      search_payloads_or_confirm1)
    # search_message_id1 = search_payload_or_confirm_response1[constant.CONTEXT]['message_id']
    [make_logistics_confirm_request(p) for p in search_payloads_or_confirm1]
