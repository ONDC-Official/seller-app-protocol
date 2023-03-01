from flask import g, request
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource, reqparse
from jsonschema import validate

from main import constant
from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

cancellation_reasons_namespace = Namespace('cancellation_reasons', description='Cancellation Reasons Namespace')


@cancellation_reasons_namespace.route("/v1/cancellation_reasons")
class CancellationReasons(Resource):
    path_schema = get_json_schema_for_given_path('/cancellation_reasons')

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/cancellation_reasons')
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.RETAIL.value)
        message = {
            "request_type": "cancellation_reasons",
            "message_ids": {
                "cancellation_reasons": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp
