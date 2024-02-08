from flask import request
from flask_restx import Namespace, Resource

from main import constant
from main.logger.custom_logging import log
from main.models.ondc_request import OndcDomain, OndcAction
from main.service.common import dump_request_payload
from main.service.retail import send_retail_payload_to_client
from main.utils.decorators import validate_auth_header
from main.utils.validation import validate_payload_schema_based_on_version

retail_ondc_network_namespace = Namespace(
    "retail_ondc_network", description="Retail ONDC Network Namespace")


@retail_ondc_network_namespace.route("/v1/search")
class SearchRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        log(f"getting search request {request_payload}")
        resp = validate_payload_schema_based_on_version(
            request_payload, "search")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload[constant.CONTEXT]["action"])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            log(f"sending Nack for search request {request_payload}")
            return resp


@retail_ondc_network_namespace.route("/v1/select")
class SelectRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "select")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/init")
class InitRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "init")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/confirm")
class ConfirmRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "confirm")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/cancel")
class CancelRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "cancel")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/cancellation_reasons")
class CancellationReasonsRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "cancellation_reasons")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/issue")
class IssueRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "issue")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        return resp


@retail_ondc_network_namespace.route("/v1/issue_status")
class IssueStatusRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "issue_status")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        return resp


@retail_ondc_network_namespace.route("/v1/rating")
class RatingRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "rating")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/status")
class StatusRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "status")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/support")
class SupportRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "support")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/track")
class TrackRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "track")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp


@retail_ondc_network_namespace.route("/v1/update")
class UpdateRequest(Resource):

    @validate_auth_header
    def post(self):
        request_payload = request.get_json()
        resp = validate_payload_schema_based_on_version(
            request_payload, "update")
        dump_request_payload(request_payload, domain=OndcDomain.RETAIL.value,
                             action=request_payload['context']['action'])
        if resp is None:
            return send_retail_payload_to_client(request_payload,
                                                 request_type=OndcAction(request_payload['context']['action']))
        else:
            return resp
