import importlib.util
import json
import logging
import os
from typing import Any, Generator
from unittest.mock import MagicMock, patch

from app.utils.input_types import InputChat
# from google.auth import exceptions as google_auth_exceptions
# from google.auth.credentials import Credentials
from httpx import AsyncClient
from langchain_core.messages import HumanMessage
import pytest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def sample_input_chat() -> InputChat:
    return InputChat(
        messages=[HumanMessage(content="What is the meaning of life?")],
        user_id="user_id",
        session_id="session_id",
    )


class AsyncIterator:
    """
    A helper class to create asynchronous iterators for testing.
    """

    def __init__(self, seq: list) -> None:
        self.iter = iter(seq)

    def __aiter__(self) -> "AsyncIterator":
        return self

    async def __anext__(self) -> Any:
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration
        

def test_redirect_root_to_docs() -> None:
    """
    Test that the root endpoint (/) redirects to the Swagger UI documentation.
    """
    with patch("app.server.chain") as _:
        from app.server import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert "Swagger UI" in response.text


@pytest.mark.asyncio
async def test_stream_chat_events() -> None:
    """
    Test the stream_events endpoint to ensure it correctly handles
    streaming responses and generates the expected events.
    """
    from app.server import app

    input_data = {
        "input": {
            "user_id": "test-user",
            "session_id": "test-session",
            "messages": [
                {"type": "human", "content": "Hello, AI!"},
                {"type": "ai", "content": "Hello!"},
                {"type": "human", "content": "What cooking recipes do you suggest?"},
            ],
        }
    }

    mock_events = [
        {"event": "on_chat_model_stream", "data": {"content": "Mocked response"}},
        {"event": "on_chat_model_stream", "data": {"content": "Additional response"}},
    ]

    with patch("app.server.chain") as mock_chain:
        mock_chain.astream_events.return_value = AsyncIterator(mock_events)

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/stream_events", json=input_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

        events = []
        for event in response.iter_lines():
            events.append(json.loads(event))

        assert len(events) == 4
        assert events[0]["event"] == "metadata"
        assert events[1]["event"] == "on_chat_model_stream"
        assert events[1]["data"]["content"] == "Mocked response"
        assert events[2]["event"] == "on_chat_model_stream"
        assert events[2]["data"]["content"] == "Additional response"
        assert events[3]["event"] == "end"
