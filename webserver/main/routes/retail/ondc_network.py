from flask import request
from flask_restx import Namespace, Resource

from main import constant
from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.service.utils import validate_auth_header
from main.utils.validation import validate_payload_schema_based_on_version

retail_ondc_network_namespace = Namespace("retail_ondc_network", description="Retail ONDC Network Namespace")


@retail_ondc_network_namespace.route("/v1/search")
class SearchRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "search")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value)
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_search",
                "message_ids": {
                    "search": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/select")
class SelectRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "select")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_select",
                "message_ids": {
                    "select": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/init")
class InitRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "init")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_init",
                "message_ids": {
                    "init": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/confirm")
class ConfirmRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "confirm")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_confirm",
                "message_ids": {
                    "confirm": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/cancel")
class CancelRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "cancel")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_cancel",
                "message_ids": {
                    "cancel": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/cancellation_reasons")
class CancellationReasonsRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "cancellation_reasons")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_cancellation_reasons",
                "message_ids": {
                    "cancellation_reasons": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/issue")
class IssueRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "issue")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_issue",
                "message_ids": {
                    "issue": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/issue_status")
class IssueStatusRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "issue_status")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_issue_status",
                "message_ids": {
                    "issue_status": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/rating")
class RatingRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "rating")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_rating",
                "message_ids": {
                    "rating": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/status")
class StatusRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "status")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_status",
                "message_ids": {
                    "status": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/support")
class SupportRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "support")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_support",
                "message_ids": {
                    "support": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/track")
class TrackRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "track")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_track",
                "message_ids": {
                    "track": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/update")
class UpdateRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "update")
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_update",
                "message_ids": {
                    "update": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp
