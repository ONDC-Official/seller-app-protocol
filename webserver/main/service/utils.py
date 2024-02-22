import hashlib
import random
import string
import uuid
from datetime import datetime

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


def make_request_over_ondc_network(payload, end_point, action, headers={}):
    log(f"Making request over ondc network on {end_point} with action {action}")
    url_with_route = f"{end_point}{action}" \
        if end_point.endswith("/") \
        else f"{end_point}/{action}"
    auth_header = create_authorisation_header(payload)
    headers['Authorization'] = auth_header
    response, status_code = post_on_bg_or_bap(url_with_route, payload, headers=headers)
    return response, status_code
