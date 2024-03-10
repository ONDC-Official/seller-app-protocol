from flask import request
from flask_restx import Namespace, Resource

from main import constant
from main.models.ondc_request import OndcDomain, OndcAction
from main.service.common import dump_request_payload
from main.service.logistics import send_logistics_payload_to_client
from main.utils.decorators import validate_auth_header
from main.utils.validation import validate_payload_schema_based_on_version
from main.service.retail import send_retail_payload_to_client_logistics
from main.logger.custom_logging import log

logistics_ondc_network_namespace = Namespace("logistics_ondc_network", description="Logistics ONDC Network Namespace")


@logistics_ondc_network_namespace.route("/v1/on_search")
class OnSearchRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_search", domain="logistics")
        if resp is None:
            log(f"On search request here is {request_payload['context']}")
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_select")
class OnSelectRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_select", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_SELECT)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_init")
class OnInitRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_init", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_INIT)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_confirm")
class OnConfirmRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        log(f"request payload for on_confirm {request_payload}")
        resp = validate_payload_schema_based_on_version(request_payload, "on_confirm", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_CONFIRM)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_cancel")
class OnCancelRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_cancel", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_CANCEL)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_cancellation_reasons")
class OnCancellationReasonsRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_cancellation_reasons", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_CANCELLATION_REASONS)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_issue")
class OnIssueRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_issue", domain="logistics")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                 action=request_payload[constant.CONTEXT]["action"])
            return send_retail_payload_to_client_logistics(request_payload,
                                                           request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_issue_status")
class OnIssueStatusRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_issue_status", domain="logistics")
        if resp is None:
            dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                 action=request_payload[constant.CONTEXT]["action"])
            return send_retail_payload_to_client_logistics(request_payload,
                                                           request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_rating")
class OnRatingRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_rating", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_RATING)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_status")
class OnStatusRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_status", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_STATUS)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_support")
class OnSupportRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_support", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_SUPPORT)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_track")
class OnTrackRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_track", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_TRACK)
            return final_resp
        else:
            return resp


@logistics_ondc_network_namespace.route("/v1/on_update")
class OnUpdateRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(request_payload, "on_update", domain="logistics")
        if resp is None:
            final_resp = dump_request_payload(request_payload, domain=OndcDomain.LOGISTICS.value,
                                              action=request_payload[constant.CONTEXT]["action"])
            send_logistics_payload_to_client(request_payload, OndcAction.ON_UPDATE)
            return final_resp
        else:
            return resp
