import json

from pika.exceptions import AMQPConnectionError
from retry import retry

from main.config import get_config_by_name
from main.models import init_database
from main.models.ondc_request import OndcDomain, OndcAction
from main.service.retail import send_retail_payload_to_client, send_retail_response_to_ondc_network
from main.service.logistics import make_logistics_request
from main.utils.rabbitmq_utils import create_channel, declare_queue, consume_message, open_connection

from main.service.common import send_logistics_on_call_count_to_client


def consume_fn(message_string):
    payload = json.loads(message_string)
    request_type = payload.get('request_type')
    parts = request_type.split("_", maxsplit=1)
    domain, action = parts[0], parts[1]
    if domain == OndcDomain.RETAIL.value:
        if "_on_" not in request_type:
            send_retail_payload_to_client(payload, request_type=OndcAction(action))
        else:
            send_retail_response_to_ondc_network(payload, request_type=OndcAction(action))
    else:
        if "_on_" not in request_type:
            make_logistics_request(payload, request_type=OndcAction(action))
        else:
            send_logistics_on_call_count_to_client(payload, request_type=OndcAction(action))


@retry(AMQPConnectionError, delay=5, jitter=(1, 3))
def run_consumer():
    init_database()
    queue_name = get_config_by_name('RABBITMQ_QUEUE_NAME')
    connection = open_connection()
    channel = create_channel(connection)
    declare_queue(channel, queue_name)
    consume_message(connection, channel, queue_name=queue_name,
                    consume_fn=consume_fn)


if __name__ == "__main__":
    run_consumer()
