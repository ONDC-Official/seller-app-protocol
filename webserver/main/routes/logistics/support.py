from flask import g, request
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource
from jsonschema import validate

from main import constant
from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

logistics_support_namespace = Namespace('logistics_support', description='Logistics Support Namespace')


@logistics_support_namespace.route("/logistics/v1/support")
class Search(Resource):
    path_schema = get_json_schema_for_given_path('/support', domain="logistics")

    @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/support', domain="logistics")
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_support",
            "message_ids": {
                "support": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp


@logistics_support_namespace.route("/logistics/v1/on_support")
class OnSupport(Resource):
    path_schema = get_json_schema_for_given_path('/on_support', domain="logistics")

    @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/on_support', domain="logistics")
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_on_support",
            "message_ids": {
                "on_support": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp

