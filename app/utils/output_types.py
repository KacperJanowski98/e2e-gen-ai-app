from typing import Dict, Literal
import uuid

from langchain_core.messages import AIMessageChunk, ToolMessage
from pydantic import BaseModel, Field


class BaseCustomChainEvent(BaseModel):
    """Base class for custom chain events."""

    name: str = "custom_chain_event"

    class Config:
        """Allow extra fields in the model."""

        extra = "allow"


class OnToolStartEvent(BaseCustomChainEvent):
    """Event representing the start of a tool execution."""

    event: Literal["on_tool_start"] = "on_tool_start"
    input: Dict = {}
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class ToolData(BaseModel):
    """Data structure for tool input and output."""

    input: Dict = {}
    output: ToolMessage


class OnToolEndEvent(BaseCustomChainEvent):
    """Event representing the end of a tool execution."""

    event: Literal["on_tool_end"] = "on_tool_end"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    data: ToolData


class ChatModelStreamData(BaseModel):
    """Data structure for chat model stream chunks."""

    chunk: AIMessageChunk


class OnChatModelStreamEvent(BaseCustomChainEvent):
    """Event representing a chunk of streamed chat model output."""

    event: Literal["on_chat_model_stream"] = "on_chat_model_stream"
    data: ChatModelStreamData


class Event(BaseModel):
    """Generic event structure."""

    event: str = "data"
    data: dict


class EndEvent(BaseModel):
    """Event representing the end of a stream."""

    event: Literal["end"] = "end"
