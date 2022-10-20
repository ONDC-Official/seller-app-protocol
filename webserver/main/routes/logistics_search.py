from flask import g, request
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource, reqparse
from jsonschema import validate

from main import constant
from main.repository.ack_response import get_ack_response
from main.service.common import dump_request_payload

logistics_search_namespace = Namespace('logistics_search', description='Search Namespace')


@logistics_search_namespace.route("/v1/on_search")
class SearchCatalogues(Resource):
    # path_schema = get_json_schema_for_given_path('/search')

    # @expects_json(path_schema)
    def post(self):
        # response_schema = get_json_schema_for_response('/search')
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, "logistics_on_search")
        # validate(resp, response_schema)
        return resp

