import logging

from app.chain import chain
from langchain_core.messages import AIMessageChunk, HumanMessage
import pytest

CHAIN_NAME = "Default"


@pytest.mark.asyncio
async def test_default_chain_astream_events() -> None:
    """
    Integration testing example for the default dummy chain. We assert that the chain returns events,
    containing AIMessageChunks.
    """
    user_message = HumanMessage(f"Test message for {CHAIN_NAME} chain")
    input_dict = {"messages": [user_message]}

    events = [event async for event in chain.astream_events(input_dict, version="v2")]

    assert len(events) > 1, (
        f"Expected multiple events for {CHAIN_NAME} chain, " f"got {len(events)}"
    )

    on_chain_stream_events = [
        event for event in events if event["event"] == "on_chat_model_stream"
    ]

    assert on_chain_stream_events, (
        f"Expected at least one on_chat_model_stream event" f" for {CHAIN_NAME} chain"
    )

    for event in on_chain_stream_events:
        assert AIMessageChunk.model_validate(
            event["data"]["chunk"]
        ), f"Invalid AIMessageChunk for {CHAIN_NAME} chain: {event['data']['chunk']}"

    logging.info(f"All assertions passed for {CHAIN_NAME} chain")
