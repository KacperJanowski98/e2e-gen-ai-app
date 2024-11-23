import json
import logging
from typing import AsyncGenerator
import uuid

from app import chain
from app.utils.input_types import Feedback, Input, InputChat, default_serialization
from app.utils.output_types import EndEvent, Event
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse

# Default chain
# from app.chain import chain

# TODO: Add another pattern

# The events that are supported by the UI Fronted
SUPPORTED_EVENTS = [
    "on_tool_start",
    "on_tool_end",
    "on_retriever_start",
    "on_retriever_end",
    "on_chat_model_stream",
]

# Initialize FastAPI app and logging
app = FastAPI()
logger = logging.basicConfig(level=logging.INFO)


async def stream_event_response(input_chat: InputChat) -> AsyncGenerator[str, None]:
    """"Stream events in response to an input chat."""
    run_id = uuid.uuid4()
    input_dict = input_chat.model_dump()

    yield json.dumps(
        Event(event="metadata", data={"run_id": str(run_id)}),
        default=default_serialization,
    ) + "\n"

    async for data in chain.astream_events(input_dict, version="v2"):
        if data["event"] in SUPPORTED_EVENTS:
            yield json.dumps(data, default=default_serialization) + "\n"

    yield json.dumps(EndEvent(), default=default_serialization) + "\n" 

# Routes
@app.get("/")
async def redirect_root_to_docs() -> RedirectResponse:
    """Redirect the root URL to the API documentation."""
    return RedirectResponse("/docs")


@app.post("/feedback")
async def collect_feedback(feedback_dict: Feedback) -> None:
    """Collect and log feedback."""
    logger.log_struct(feedback_dict.model_dump(), severity="INFO")


@app.post("/stream_events")
async def stream_chat_events(request: Input) -> StreamingResponse:
    """Stream chat events in response to an input request."""
    return StreamingResponse(
        stream_event_response(input_chat=request.input), media_type="text/event-stream"
    )


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
