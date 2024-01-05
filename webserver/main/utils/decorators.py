import json
import traceback

from main import constant
from main.config import get_config_by_name

# from flask_expects_json import expects_json
# from jsonschema.exceptions import ValidationError
#
#
# def expects_json_handling_validation(*args, **kwargs):
#     try:
#         return expects_json(*args, **kwargs)
#     except:
#         print("comig here")
from main.logger.custom_logging import log_error
from main.repository.ack_response import get_ack_response
from main.utils.cryptic_utils import verify_authorisation_header
from main.utils.lookup_utils import get_sender_public_key_from_header


def check_for_exception(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error("Something went wrong!")
            return {"error": str(e)}

    return _wrapper


def validate_auth_header(func):
    from flask import request

    def wrapper(*args, **kwargs):
        if get_config_by_name("VERIFICATION_ENABLE"):
            auth_header = request.headers.get('Authorization')
            domain = request.get_json().get("context", {}).get("domain")
            if auth_header and verify_authorisation_header(auth_header, request.data.decode("utf-8"),
                                                           public_key=get_sender_public_key_from_header(auth_header, domain)):
                return func(*args, **kwargs)
            context = json.loads(request.data)[constant.CONTEXT]
            return get_ack_response(context=context, ack=False, error={
                "code": "10001",
                "message": "Invalid Signature"
            }), 401
        else:
            return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
