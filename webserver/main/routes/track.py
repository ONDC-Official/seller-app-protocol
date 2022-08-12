from flask_expects_json import expects_json
from flask_restx import Namespace, Resource, reqparse
from jsonschema import validate

from main.repository.ack_response import get_ack_response
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

track_namespace = Namespace('track', description='Track Namespace')


@track_namespace.route("/v1/track")
class TrackOrder(Resource):
    path_schema = get_json_schema_for_given_path('/track')

    @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/track')
        resp = get_ack_response(ack=True)
        validate(resp, response_schema)
        return resp
