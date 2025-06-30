import threading
import time
import pytest
from app.messaging.rabbitmq import publish_client_created, consume_client_created

@pytest.mark.integration
def test_rabbitmq_publish_and_consume_real():
    received = []

    def handler(msg):
        received.append(msg)

    thread = threading.Thread(target=lambda: consume_client_created(handler), daemon=True)
    thread.start()

    time.sleep(1)  # laisser le consumer démarrer
    test_data = {"name": "IntegrationTest", "email": "int@test.com"}
    publish_client_created(test_data)

    time.sleep(2)  # laisser le message être consommé

    assert any(msg["email"] == "int@test.com" for msg in received)
