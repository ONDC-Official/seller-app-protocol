import pika
from flask import g, request
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource, reqparse
from jsonschema import validate

from main import constant
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

select_namespace = Namespace('select', description='Select Namespace')


@select_namespace.route("/v1/select")
class SelectOrder(Resource):
    path_schema = get_json_schema_for_given_path('/select')

    @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/select')
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, "select")
        # send_message_to_queue_for_given_request('select', g.data)
        send_message_to_queue_for_given_request("select_1", payload[constant.CONTEXT]["transaction_id"],
                                                properties=pika.BasicProperties(headers={
                                                    "x-delay": 0
                                                }))
        validate(resp, response_schema)
        return resp
