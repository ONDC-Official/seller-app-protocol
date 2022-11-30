from flask_restx import Namespace, Resource, reqparse

from main.service.common import get_network_request_payloads

response_namespace = Namespace('response', description='Response Namespace')


@response_namespace.route("/v1/response/network-request-payloads")
class GetNetworkRequestPayloads(Resource):

    def create_parser_with_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument("select", dest='retail_select', required=False)
        parser.add_argument("logisticsOnSearch", dest="logistics_on_search", required=False)
        return parser.parse_args()

    def get(self):
        args = self.create_parser_with_args()
        return get_network_request_payloads(**args)

