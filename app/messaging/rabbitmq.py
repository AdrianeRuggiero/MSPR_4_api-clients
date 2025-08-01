import json
import pika
import logging
from app.config import settings
from app.messaging.schemas import (
    ClientCreatedMessage, ClientUpdatedMessage, ClientDeletedMessage,
)

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_channel():
    connection_params = pika.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    # Déclaration des différentes queues
    channel.queue_declare(queue='client_created', durable=True)
    channel.queue_declare(queue='client_updated', durable=True)
    channel.queue_declare(queue='client_deleted', durable=True)
    return channel

# Publier un client créé
def publish_client_created(client_data: dict, channel=None):
    validated = ClientCreatedMessage(**client_data)
    if channel is None:
        channel = get_channel()
    logger.info(f"[RabbitMQ] Publication dans 'client_created' : {validated.dict()}")
    channel.basic_publish(
        exchange='',
        routing_key='client_created',
        body=validated.model_dump_json(),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    channel.close()

# Publier un client mis à jour
def publish_client_updated(client_data: dict, channel=None):
    validated = ClientUpdatedMessage(**client_data)
    if channel is None:
        channel = get_channel()
    logger.info(f"[RabbitMQ] Publication dans 'client_updated' : {validated.dict()}")
    channel.basic_publish(
        exchange='',
        routing_key='client_updated',
        body=validated.model_dump_json(),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    channel.close()

# Publier un client supprimé
def publish_client_deleted(client_id: str, channel=None):
    validated = ClientDeletedMessage(_id=client_id)
    if channel is None:
        channel = get_channel()
    logger.info(f"[RabbitMQ] Publication dans 'client_deleted' : {validated.dict()}")
    channel.basic_publish(
        exchange='',
        routing_key='client_deleted',
        body=validated.model_dump_json(),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    channel.close()

# Consommateur pour 'client_created'
def consume_client_created(callback):
    channel = get_channel()

    def wrapper(ch, method, properties, body):
        data = json.loads(body)
        logger.info(f"[RabbitMQ] Message reçu de 'client_created' : {data}")
        callback(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='client_created', on_message_callback=wrapper)
    logger.info("[RabbitMQ] En attente de messages sur 'client_created'. CTRL+C pour arrêter.")
    channel.start_consuming()
