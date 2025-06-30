from unittest.mock import MagicMock, patch
import json
from app.messaging.rabbitmq import (
    publish_client_created,
    consume_client_created
)
from app.messaging.schemas import ClientCreatedMessage
import pytest

def test_publish_client_created():
    mock_channel = MagicMock()
    data = {
        "name": "Test",
        "email": "test@example.com",
        "company": "TestCorp",
        "phone": "+33123456789",
        "is_active": True
    }
    publish_client_created(data, channel=mock_channel)

    mock_channel.basic_publish.assert_called_once()
    mock_channel.close.assert_called_once()

def test_consume_client_created_callback_wrapper():
    mock_callback = MagicMock()
    mock_channel = MagicMock()
    mock_body = json.dumps({"name": "CallbackTest"}).encode()
    mock_method = MagicMock()
    mock_method.delivery_tag = "abc123"

    with patch("app.messaging.rabbitmq.get_channel", return_value=mock_channel):
        consume_client_created(mock_callback)
        args, kwargs = mock_channel.basic_consume.call_args
        wrapper_func = kwargs["on_message_callback"]

        wrapper_func(mock_channel, mock_method, None, mock_body)

        mock_callback.assert_called_once_with({"name": "CallbackTest"})
        mock_channel.basic_ack.assert_called_once_with(delivery_tag="abc123")

@patch("app.messaging.rabbitmq.get_channel")
def test_publish_client_updated(mock_get_channel):
    mock_channel = MagicMock()
    mock_get_channel.return_value = mock_channel

    from app.messaging.rabbitmq import publish_client_updated
    data = {
        "_id": "abc123",
        "name": "Updated",
        "email": "update@example.com",
        "company": "NewCorp",
        "phone": "+33111111111",
        "is_active": False
    }
    publish_client_updated(data)

    mock_channel.basic_publish.assert_called_once()
    mock_channel.close.assert_called_once()

@patch("app.messaging.rabbitmq.get_channel")
def test_publish_client_deleted(mock_get_channel):
    mock_channel = MagicMock()
    mock_get_channel.return_value = mock_channel

    from app.messaging.rabbitmq import publish_client_deleted
    publish_client_deleted("some-client-id")

    mock_channel.basic_publish.assert_called_once()
    mock_channel.close.assert_called_once()

@patch("pika.BlockingConnection")
def test_get_channel(mock_connection):
    mock_channel = MagicMock()
    mock_connection.return_value.channel.return_value = mock_channel

    from app.messaging.rabbitmq import get_channel
    channel = get_channel()

    mock_channel.queue_declare.assert_any_call(queue="client_created", durable=True)
    mock_channel.queue_declare.assert_any_call(queue="client_updated", durable=True)
    mock_channel.queue_declare.assert_any_call(queue="client_deleted", durable=True)

def test_client_created_message_valid():
    data = {
        "name": "Alice",
        "email": "alice@example.com",
        "company": "CoolCorp",
        "phone": "+33612345678",
        "is_active": True
    }
    msg = ClientCreatedMessage(**data)
    assert msg.email == "alice@example.com"

def test_client_created_message_invalid_email():
    with pytest.raises(ValueError):
        ClientCreatedMessage(name="X", email="bademail", is_active=True)
