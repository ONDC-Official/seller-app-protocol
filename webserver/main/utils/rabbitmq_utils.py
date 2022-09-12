import pika

from main.config import get_config_by_name
from main.logger.custom_logging import log, log_error


def open_connection():
    rabbitmq_host = get_config_by_name('RABBITMQ_HOST')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, heartbeat=10))
    return connection


def close_connection(connection):
    connection.close()


def create_channel():
    connection = open_connection()
    channel = connection.channel()
    return channel


def declare_queue(channel, queue_name):
    channel.queue_declare(queue=queue_name)


def publish_message_to_queue(channel, exchange, routing_key, body):
    log(f"Publishing message of {body}")
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)


def consume_message(channel, queue_name, consume_fn):
    def callback(ch, method, properties, body):
        try:
            log(f"Got message {body} !")
            consume_fn(body)
            channel.basic_ack(method.delivery_tag)
        except:
            log_error(f"Something went wrong for {body} !")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    log('Waiting for messages:')
    channel.start_consuming()
