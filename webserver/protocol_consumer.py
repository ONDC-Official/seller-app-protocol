import json

from pika.exceptions import AMQPConnectionError
from retry import retry

from main.config import get_config_by_name
from main.service.confirm_service import make_logistics_confirm_or_send_bpp_failure_response, \
    send_confirm_response_to_bap
from main.service.init_service import make_logistics_init_or_send_bpp_failure_response, send_init_response_to_bap
from main.service.select_service import make_logistics_search_or_send_bpp_failure_response, send_select_response_to_bap
from main.service.support_service import make_logistics_support_or_send_bpp_failure_response, \
    send_support_response_to_bap
from main.service.track_service import make_logistics_track_or_send_bpp_failure_response, send_track_response_to_bap
from main.service.status_service import make_logistics_status_or_send_bpp_failure_response, send_status_response_to_bap
from main.utils.rabbitmq_utils import create_channel, declare_queue, consume_message, open_connection

from main.service.common import send_bpp_responses_to_bg_or_bpp


request_type_to_function_mapping = {
    "retail_search": send_bpp_responses_to_bg_or_bpp,
    "retail_select": make_logistics_search_or_send_bpp_failure_response,
    "retail_on_select": send_select_response_to_bap,
    "retail_init": make_logistics_init_or_send_bpp_failure_response,
    "retail_on_init": send_init_response_to_bap,
    "retail_confirm": make_logistics_confirm_or_send_bpp_failure_response,
    "retail_on_confirm": send_confirm_response_to_bap,
    "retail_track": make_logistics_track_or_send_bpp_failure_response,
    "retail_on_track": send_track_response_to_bap,
    "retail_status": make_logistics_status_or_send_bpp_failure_response,
    "retail_on_status": send_status_response_to_bap,
    "retail_support": make_logistics_support_or_send_bpp_failure_response,
    "retail_on_support": send_support_response_to_bap,
}


def consume_fn(message_string):
    payload = json.loads(message_string)
    request_type = payload.get('request_type')
    request_type_consume_fn = request_type_to_function_mapping.get(request_type, send_bpp_responses_to_bg_or_bpp)
    request_type_consume_fn(payload)


@retry(AMQPConnectionError, delay=5, jitter=(1, 3))
def run_consumer():
    queue_name = get_config_by_name('RABBITMQ_QUEUE_NAME')
    connection = open_connection()
    channel = create_channel(connection)
    declare_queue(channel, queue_name)
    consume_message(connection, channel, queue_name=queue_name, consume_fn=consume_fn)


if __name__ == "__main__":
    run_consumer()

