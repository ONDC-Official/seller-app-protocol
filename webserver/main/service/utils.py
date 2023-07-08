import hashlib
import json
import os
import random
import string
import uuid
from datetime import datetime

from flask import request
from flask_restx import abort

from main import constant
from main.config import get_config_by_name
from main.repository.ack_response import get_ack_response
from main.utils.cryptic_utils import verify_authorisation_header
from main.utils.lookup_utils import get_bap_public_key_from_header
from main.logger.custom_logging import log
from main.utils.cryptic_utils import create_authorisation_header
from main.utils.webhook_utils import post_on_bg_or_bap

URL_SPLITTER = "?"


def get_unique_id(entity_prefix):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{entity_prefix}_{current_time}_{str(uuid.uuid4())}"


def create_random_number(num_digit=6):
    return "".join([random.choice(string.digits) for i in range(num_digit)])


def create_random_string(num_digit=6):
    return "".join([random.choice(string.ascii_lowercase) for i in range(num_digit)])


def create_random_alpha_numeric_string(num_digit=6):
    return "".join([random.choice(string.ascii_lowercase + string.digits) for i in range(num_digit)])


def create_ever_increasing_random_number(num_digit=6):
    return str(datetime.now().timestamp())[:num_digit]


def password_hash(incoming_password):
    incoming_password = incoming_password or ""
    h = hashlib.md5(incoming_password.encode())
    return h.hexdigest()


def handle_stop_iteration(func):
    def exception_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except StopIteration:
            log(f"element not found with {args} and {kwargs}")
            abort(message="Failed while querying and updating SQL server")

    return exception_handler


def validate_auth_header(func):
    def wrapper(*args, **kwargs):
        if get_config_by_name("VERIFICATION_ENABLE"):
            auth_header = request.headers.get('Authorization')
            if auth_header and verify_authorisation_header(auth_header, request.data.decode("utf-8"),
                                                           public_key=get_bap_public_key_from_header(auth_header)):
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


def make_request_over_ondc_network(payload, end_point, action):
    log(f"Making request over ondc network on {end_point} with action {action}")
    url_with_route = f"{end_point}{action}" \
        if end_point.endswith("/") \
        else f"{end_point}/{action}"
    auth_header = create_authorisation_header(payload)
    status_code = post_on_bg_or_bap(url_with_route, payload, headers={'Authorization': auth_header})
    return status_code
