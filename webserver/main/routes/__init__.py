import json
import os

from flask import request
from flask_restx import Api as BaseAPI
from jsonschema import ValidationError
from werkzeug.exceptions import BadRequest

from main import constant
from main.models.error import BaseError
from main.repository.ack_response import get_ack_response

from main.routes.logistics.client import logistics_client_namespace
from main.routes.logistics.ondc_network import logistics_ondc_network_namespace
from main.routes.response import response_namespace
from main.routes.retail.ondc_network import retail_ondc_network_namespace
from main.routes.retail.client import retail_client_namespace
from main.utils.schema_utils import transform_json_schema_error


class Api(BaseAPI):
    def _register_doc(self, app_or_blueprint):
        # HINT: This is just a copy of the original implementation with the last line commented out.
        if self._add_specs and self._doc:
            # Register documentation before root if enabled
            app_or_blueprint.add_url_rule(self._doc, 'doc', self.render_doc)
        # app_or_blueprint.add_url_rule(self._doc, 'root', self.render_root)

    @property
    def base_path(self):
        return ''


api = Api(
    title='ONDC API',
    version='1.0',
    description='Rest api for ONDC dashboard project',
    doc='/swagger/' if os.getenv("ENV") != None else False
)

# api.render_root()


@api.errorhandler(BadRequest)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        context = json.loads(request.data)[constant.CONTEXT]
        error_message = transform_json_schema_error(error.description)
        return get_ack_response(context=context, ack=False,
                                error={"type": BaseError.JSON_SCHEMA_ERROR.value, "message": error_message}), 400
    # handle other "Bad Request"-errors
    return str(error), 500


@api.errorhandler(ValidationError)
def bad_request(error):
    return {'error': str(error), 'message': error.message}, 400


api.add_namespace(response_namespace, path='/protocol')
api.add_namespace(retail_ondc_network_namespace, path='/protocol')
api.add_namespace(retail_client_namespace, path='/protocol')
api.add_namespace(logistics_ondc_network_namespace, path='/protocol/logistics')
api.add_namespace(logistics_client_namespace, path='/protocol/logistics')
