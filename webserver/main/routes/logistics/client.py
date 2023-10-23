from flask import request
from flask_restx import Namespace, Resource

from main import constant
from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.validation import validate_payload_schema_based_on_version

logistics_client_namespace = Namespace("logistics_client", description="Logistics Client Namespace")


@logistics_client_namespace.route("/v1/search")
class SearchRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "search", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_search",
                "message_ids": {
                    "search": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/select")
class SelectRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "select", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_select",
                "message_ids": {
                    "select": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/init")
class InitRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "init", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_init",
                "message_ids": {
                    "init": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/confirm")
class ConfirmRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "confirm", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_confirm",
                "message_ids": {
                    "confirm": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/cancel")
class CancelRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "cancel", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_cancel",
                "message_ids": {
                    "cancel": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/cancellation_reasons")
class CancellationReasonsRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "cancellation_reasons", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_cancellation_reasons",
                "message_ids": {
                    "cancellation_reasons": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/issue")
class IssueRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "issue", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_issue",
                "message_ids": {
                    "issue": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/issue_status")
class IssueStatusRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "issue_status", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_issue_status",
                "message_ids": {
                    "issue_status": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/rating")
class RatingRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "rating", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
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


@logistics_client_namespace.route("/v1/status")
class StatusRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "status", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_status",
                "message_ids": {
                    "status": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/support")
class SupportRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "support", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
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


@logistics_client_namespace.route("/v1/track")
class TrackRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "track", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_track",
                "message_ids": {
                    "track": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_client_namespace.route("/v1/update")
class UpdateRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "update", domain="logistics")
        dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value, action=request_payload['context']['action'])
        if resp is None:
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_update",
                "message_ids": {
                    "update": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp
