import json

from pika.exceptions import AMQPConnectionError
from retry import retry

from main.config import get_config_by_name
from main.service.cancel_service import send_cancel_payload_to_client, make_logistics_cancel, \
    send_cancel_response_to_bap
from main.service.confirm_service import send_confirm_payload_to_client, make_logistics_confirm, \
    send_confirm_response_to_bap
from main.service.init_service import send_init_payload_to_client, make_logistics_init, send_init_response_to_bap
from main.service.search_service import send_search_response_to_gateway, send_search_payload_to_client
from main.service.select_service import send_select_payload_to_client, make_logistics_search, \
    send_select_response_to_bap
from main.service.support_service import send_support_payload_to_client, make_logistics_support, \
    send_support_response_to_bap
from main.service.track_service import send_track_payload_to_client, make_logistics_track, send_track_response_to_bap
from main.service.status_service import send_status_payload_to_client, make_logistics_status, \
    send_status_response_to_bap
from main.service.update_service import send_update_response_to_bap, make_logistics_update, \
    send_update_payload_to_client
from main.service.issue_service import send_issue_response_to_bap, make_logistics_issue, \
    send_issue_payload_to_client
from main.service.issue_status_service import send_issue_status_response_to_bap, make_logistics_issue_status, \
    send_issue_status_payload_to_client
from main.utils.rabbitmq_utils import create_channel, declare_queue, consume_message, open_connection

from main.service.common import send_bpp_responses_to_bg_or_bpp, send_logistics_on_call_count_to_client

request_type_to_function_mapping = {
    "retail_search": send_search_payload_to_client,
    "retail_on_search": send_search_response_to_gateway,
    "retail_select": send_select_payload_to_client,
    "retail_on_select": send_select_response_to_bap,
    "retail_init": send_init_payload_to_client,
    "retail_on_init": send_init_response_to_bap,
    "retail_confirm": send_confirm_payload_to_client,
    "retail_on_confirm": send_confirm_response_to_bap,
    "retail_track": send_track_payload_to_client,
    "retail_on_track": send_track_response_to_bap,
    "retail_status": send_status_payload_to_client,
    "retail_on_status": send_status_response_to_bap,
    "retail_support": send_support_payload_to_client,
    "retail_on_support": send_support_response_to_bap,
    "retail_cancel": send_cancel_payload_to_client,
    "retail_on_cancel": send_cancel_response_to_bap,
    "retail_update": send_update_payload_to_client,
    "retail_on_update": send_update_response_to_bap,
    "retail_issue": send_issue_payload_to_client,
    "retail_on_issue": send_issue_response_to_bap,
    "retail_issue_status": send_issue_status_payload_to_client,
    "retail_on_issue_status": send_issue_status_response_to_bap,

    "logistics_search": make_logistics_search,
    "logistics_init": make_logistics_init,
    "logistics_confirm": make_logistics_confirm,
    "logistics_track": make_logistics_track,
    "logistics_status": make_logistics_status,
    "logistics_support": make_logistics_support,
    "logistics_cancel": make_logistics_cancel,
    "logistics_update": make_logistics_update,
    "logistics_issue": make_logistics_issue,
    "logistics_issue_status": make_logistics_issue_status,

    "logistics_on_search": lambda m: send_logistics_on_call_count_to_client(m, "on_search"),
    "logistics_on_init": lambda m: send_logistics_on_call_count_to_client(m, "on_init"),
    "logistics_on_confirm": lambda m: send_logistics_on_call_count_to_client(m, "on_confirm"),
    "logistics_on_track": lambda m: send_logistics_on_call_count_to_client(m, "on_track"),
    "logistics_on_status": lambda m: send_logistics_on_call_count_to_client(m, "on_status"),
    "logistics_on_support": lambda m: send_logistics_on_call_count_to_client(m, "on_support"),
    "logistics_on_cancel": lambda m: send_logistics_on_call_count_to_client(m, "on_cancel"),
    "logistics_on_update": lambda m: send_logistics_on_call_count_to_client(m, "on_update"),
    "logistics_on_issue": lambda m: send_logistics_on_call_count_to_client(m, "on_issue"),
    "logistics_on_issue_status": lambda m: send_logistics_on_call_count_to_client(m, "on_issue_status"),
}


def consume_fn(message_string):
    payload = json.loads(message_string)
    request_type = payload.get('request_type')
    request_type_consume_fn = request_type_to_function_mapping.get(
        request_type, send_bpp_responses_to_bg_or_bpp)
    request_type_consume_fn(payload)


@retry(AMQPConnectionError, delay=5, jitter=(1, 3))
def run_consumer():
    queue_name = get_config_by_name('RABBITMQ_QUEUE_NAME')
    connection = open_connection()
    channel = create_channel(connection)
    declare_queue(channel, queue_name)
    consume_message(connection, channel, queue_name=queue_name,
                    consume_fn=consume_fn)


if __name__ == "__main__":
    run_consumer()
