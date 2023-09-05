from flask import request
from flask_restx import Namespace, Resource

from main import constant
from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.decorators import validate_auth_header
from main.utils.validation import validate_payload_schema_based_on_version

logistics_ondc_network_namespace = Namespace("logistics_ondc_network", description="Logistics ONDC Network Namespace")


@logistics_ondc_network_namespace.route("/v1/on_search")
class OnSearchRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_search")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_search",
                "message_ids": {
                    "on_search": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_select")
class OnSelectRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_select")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_select",
                "message_ids": {
                    "on_select": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_init")
class OnInitRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_init")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_init",
                "message_ids": {
                    "on_init": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_confirm")
class OnConfirmRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_confirm")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_confirm",
                "message_ids": {
                    "on_confirm": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_cancel")
class OnCancelRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_cancel")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_cancel",
                "message_ids": {
                    "on_cancel": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_cancellation_reasons")
class OnCancellationReasonsRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_cancellation_reasons")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_cancellation_reasons",
                "message_ids": {
                    "on_cancellation_reasons": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_issue")
class OnIssueRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_issue")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_issue",
                "message_ids": {
                    "on_issue": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_issue_status")
class OnIssueStatusRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_issue_status")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_issue_status",
                "message_ids": {
                    "on_issue_status": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_rating")
class OnRatingRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_rating")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_rating",
                "message_ids": {
                    "on_rating": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_status")
class OnStatusRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_status")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_status",
                "message_ids": {
                    "on_status": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_support")
class OnSupportRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_support")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_support",
                "message_ids": {
                    "on_support": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_track")
class OnTrackRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_track")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_track",
                "message_ids": {
                    "on_track": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_update")
class OnUpdateRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_update")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value, action=request_payload[constant.CONTEXT]["action"])
            message = {
                "request_type": f"{OndcDomain.RETAIL.value}_on_update",
                "message_ids": {
                    "on_update": request_payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            return get_ack_response(request_payload[constant.CONTEXT], ack=True)
        else:
            return resp
