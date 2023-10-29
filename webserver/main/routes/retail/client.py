from flask import request
from flask_restx import Namespace, Resource

from main.models.ondc_request import OndcAction
from main.service.retail import send_retail_response_to_ondc_network
from main.utils.validation import validate_payload_schema_based_on_version

retail_client_namespace = Namespace("retail_client", description="Retail Client Namespace")


@retail_client_namespace.route("/v1/on_search")
class OnSearchRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_search")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_select")
class OnSelectRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_select")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_init")
class OnInitRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_init")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_confirm")
class OnConfirmRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_confirm")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_cancel")
class OnCancelRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_cancel")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_cancellation_reasons")
class OnCancellationReasonsRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_cancellation_reasons")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_issue")
class OnIssueRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_issue")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_issue_status")
class OnIssueStatusRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_issue_status")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_rating")
class OnRatingRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_rating")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_status")
class OnStatusRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_status")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_support")
class OnSupportRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_support")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_track")
class OnTrackRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_track")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp


@retail_client_namespace.route("/v1/on_update")
class OnUpdateRequest(Resource):

    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_update")
        if resp is None:
            action = request_payload["context"]["action"]
            return send_retail_response_to_ondc_network(request_payload, request_type=OndcAction(action))
        else:
            return resp
