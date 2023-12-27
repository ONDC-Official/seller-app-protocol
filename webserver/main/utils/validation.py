import json

import jsonschema
import pydantic
from flask import request
from jsonschema.validators import validate

from main import constant
from main.logger.custom_logging import log
from main.models.error import BaseError
from main.repository.ack_response import get_ack_response
from main.request_models.retail import request as retail_request
from main.request_models.logistics import request as logistics_request
from main.utils.schema_utils import get_json_schema_for_given_path, transform_json_schema_error


def validate_payload_schema_based_on_version(request_payload, request_type, domain: str = "retail"):
    # Issue action's core version should be 1.0.0
    if request_payload[constant.CONTEXT]["core_version"] == "1.0.0":
        if "issue" in request_type:
            return validate_payload_schema_using_pydantic_classes(request_payload, request_type, domain)
        return validate_payload_schema_using_json_schema(request_payload, request_type)
    # Rest of the action methods should have 1.2.0
    elif request_payload[constant.CONTEXT]["core_version"] == "1.2.0":
        return validate_payload_schema_using_pydantic_classes(request_payload, request_type, domain)
    return validate_payload_schema_using_json_schema(request_payload, request_type)


def validate_payload_schema_using_json_schema(request_payload, request_type):
    try:
        request_schema = get_json_schema_for_given_path(f"/{request_type}")
        validate(request_payload, request_schema)
        return None
    except jsonschema.exceptions.ValidationError as e:
        error_message = transform_json_schema_error(e)
        context = json.loads(request.data)[constant.CONTEXT]
        return get_ack_response(context=context, ack=False,
                                error={"type": BaseError.JSON_SCHEMA_ERROR.value, "code": "20000",
                                       "message": error_message}), 400


def validate_payload_schema_using_pydantic_classes(request_payload, request_type, domain: str = "retail"):
    try:
        if domain == "retail":
            retail_request.request_type_to_class_mapping[request_type](
                **request_payload)
        else:
            logistics_request.request_type_to_class_mapping[request_type](
                **request_payload)
        return None
    except pydantic.ValidationError as e:
        error_message = str(e)
        log(e)
        context = json.loads(request.data)[constant.CONTEXT]
        return get_ack_response(context=context, ack=False,
                                error={"type": BaseError.JSON_SCHEMA_ERROR.value, "code": "20000",
                                       "message": error_message}), 400
