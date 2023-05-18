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


issue_status_namespace = Namespace(
    'issue_status', description='Issue_status Namespace')


@issue_status_namespace.route("/v1/issue_status")
class issue_statusOrder(Resource):
    path_schema = get_json_schema_for_given_path('/issue_status')

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/issue_status')
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.RETAIL.value)
        message = {
            "request_type": f"{OndcDomain.RETAIL.value}_issue_status",
            "message_ids": {
                "issue_status": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp


@issue_status_namespace.route("/v1/on_issue_status")
class OnSelectOrder(Resource):
    path_schema = get_json_schema_for_given_path('/on_issue_status')

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/on_issue_status')
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.RETAIL.value)
        message = {
            "request_type": f"{OndcDomain.RETAIL.value}_on_issue_status",
            "message_ids": {
                "on_issue_status": payload[constant.CONTEXT]["message_id"]
            }
        }
        print("message----------", message)
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp
