from flask import request
from flask_restx import Namespace, Resource

from main.models.ondc_request import OndcAction
from main.service.logistics import make_logistics_request
from main.utils.validation import validate_payload_schema_based_on_version

logistics_client_namespace = Namespace("logistics_client", description="Logistics Client Namespace")


@logistics_client_namespace.route("/v1/search")
class SearchRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "search", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/select")
class SelectRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "select", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/init")
class InitRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "init", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/confirm")
class ConfirmRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "confirm", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/cancel")
class CancelRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "cancel", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/cancellation_reasons")
class CancellationReasonsRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "cancellation_reasons", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/issue")
class IssueRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "issue", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/issue_status")
class IssueStatusRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "issue_status", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/rating")
class RatingRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "rating", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/status")
class StatusRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "status", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/support")
class SupportRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "support", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/track")
class TrackRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "track", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp


@logistics_client_namespace.route("/v1/update")
class UpdateRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "update", domain="logistics")
        if resp is None:
            action = request_payload["context"]["action"]
            return make_logistics_request(request_payload, request_type=OndcAction(action))
        else:
            return resp
