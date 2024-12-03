import logging

from app.patterns.custom_rag_qa.chain import chain
from app.utils.output_types import OnToolEndEvent
from langchain_core.messages import AIMessageChunk, HumanMessage
import pytest

CHAIN_NAME = "Rag QA"


@pytest.mark.asyncio
async def test_rag_chain_astream_events() -> None:
    """
    Integration testing example for the default RAG QA chain. We assert that the chain returns events,
    containing AIMessageChunks.
    """
    user_message = HumanMessage(f"Test message for {CHAIN_NAME} chain")
    input_dict = {"messages": [user_message]}

    events = [event async for event in chain.astream_events(input_dict, version="v2")]

    assert len(events) > 1, (
        f"Expected multiple events for {CHAIN_NAME} chain, " f"got {len(events)}"
    )

    on_tool_end_events = [event for event in events if event["event"] == "on_tool_end"]
    assert len(on_tool_end_events) == 1, (
        f"Expected exactly one on_tool_end event for {CHAIN_NAME} chain, "
        f"got {len(on_tool_end_events)}"
    )
    assert isinstance(
        OnToolEndEvent.model_validate(on_tool_end_events[0]), OnToolEndEvent
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
