import json

from main.utils.rabbitmq_utils import create_channel, declare_queue, consume_message

from main.service.common import send_bpp_responses_to_bg_or_bpp


def consume_fn(message_string):
    payload = json.loads(message_string)
    request_type = payload.pop('request_type')
    send_bpp_responses_to_bg_or_bpp(request_type, payload)


queue_name = 'bpp_protocol'
channel = create_channel()
declare_queue(channel, queue_name)
consume_message(channel, queue_name=queue_name, consume_fn=consume_fn)
