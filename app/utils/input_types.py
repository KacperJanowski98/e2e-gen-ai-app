from typing import Annotated, Any, List, Literal, Optional, Union

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, Field


class InputChat(BaseModel):
    """Represents the input for a chat session."""

    messages: List[
        Annotated[
            Union[HumanMessage, AIMessage, ToolMessage], Field(discriminator="type")
        ]
    ] = Field(
        ..., description="The chat messages representing the current conversation."
    )
    user_id: str = ""
    session_id: str = ""


class Input(BaseModel):
    """Wrapper class for InputChat."""

    input: InputChat


class Feedback(BaseModel):
    """Represents feedback for a conversation."""

    score: Union[int, float]
    text: Optional[str] = ""
    run_id: str
    log_type: Literal["feedback"] = "feedback"


def default_serialization(obj: Any) -> Any:
    """
    Default serialization for LangChain objects.
    Converts BaseModel instances to dictionaries.
    """
    if isinstance(obj, BaseModel):
        return obj.model_dump()
