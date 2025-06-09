import json
import pika
from app.config import settings

# Connexion à RabbitMQ
connection_params = pika.URLParameters(settings.RABBITMQ_URL)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Déclare une file si elle n'existe pas (ex: pour notifier la création de client)
channel.queue_declare(queue='client_created', durable=True)

# Fonction pour publier un message
def publish_client_created(client_data: dict):
    channel.basic_publish(
        exchange='',
        routing_key='client_created',
        body=json.dumps(client_data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # message persistant
        )
    )

# Consommateur générique (à lancer manuellement pour l'exemple)
def consume_client_created(callback):
    def wrapper(ch, method, properties, body):
        data = json.loads(body)
        callback(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='client_created', on_message_callback=wrapper)
    print(" [*] En attente de messages sur 'client_created'. CTRL+C pour arrêter.")
    channel.start_consuming()
