import json

from pika.exceptions import AMQPConnectionError
from retry import retry

from main.config import get_config_by_name
from main.models import init_database
from main.service.select_service import make_logistics_search_or_send_bpp_failure_response, send_select_response_to_bap
from main.utils.rabbitmq_utils import create_channel, declare_queue, consume_message, open_connection

from main.service.common import send_bpp_responses_to_bg_or_bpp


init_database()


def consume_fn(message_string):
    payload = json.loads(message_string)
    request_type = payload.get('request_type')
    if request_type == "search":
        send_bpp_responses_to_bg_or_bpp(payload)
    elif request_type == "select_1":
        make_logistics_search_or_send_bpp_failure_response(payload)
    elif request_type == "select_2":
        send_select_response_to_bap(payload)
    else:
        send_bpp_responses_to_bg_or_bpp(payload)


@retry(AMQPConnectionError, delay=5, jitter=(1, 3))
def run_consumer():
    queue_name = get_config_by_name('RABBITMQ_QUEUE_NAME')
    connection = open_connection()
    channel = create_channel(connection)
    declare_queue(channel, queue_name)
    consume_message(connection, channel, queue_name=queue_name, consume_fn=consume_fn)


if __name__ == "__main__":
    run_consumer()

