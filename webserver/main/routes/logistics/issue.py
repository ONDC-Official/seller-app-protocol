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


logistics_issue_namespace = Namespace(
    'logistics_issue', description='Logistics Issue Namespace')


@logistics_issue_namespace.route("/logistics/v1/issue")
class Issue(Resource):
    # path_schema = get_json_schema_for_given_path('/issue', domain="logistics")

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response(
            '/issue', domain="logistics")
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_issue",
            "message_ids": {
                "issue": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp


@logistics_issue_namespace.route("/logistics/v1/on_issue")
class OnInit(Resource):
    # path_schema = get_json_schema_for_given_path(
    #     '/on_issue', domain="logistics")

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response(
            '/on_issue', domain="logistics")
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_on_issue",
            "message_ids": {
                "on_issue": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp
