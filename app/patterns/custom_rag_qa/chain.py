# mypy: disable-error-code="arg-type,attr-defined"
# pylint: disable=W0613, W0622

import logging
from typing import Any, AsyncIterator, Dict, List

from app.patterns.custom_rag_qa.templates import (
    inspect_conversation_template,
    rag_template,
    template_docs,
)
from app.patterns.custom_rag_qa.vector_store import get_vector_store
from app.utils.decorators import custom_chain
from app.utils.output_types import OnChatModelStreamEvent, OnToolEndEvent
from langchain.schema import Document
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.documents.compressor import BaseDocumentCompressor


# Configuration
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3-groq-tool-use:latest"
TOP_K = 5

# Initialize logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Set up embedding model and vector store
embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)
vector_store = get_vector_store(embedding=embedding)

retriever = vector_store.as_retriever(
    search_type="mmr",  # Maximum Marginal Relevance
    search_kwargs={
        "k": TOP_K,
        "fetch_k": 20,  # Więcej dokumentów do wyboru
        "lambda_mult": 0.5  # Balans między podobieństwem a różnorodnością
    }
)

@tool
def retrieve_docs(query: str) -> List[Document]:
    """
    Useful for retrieving relevant documents based on a query.
    Use this when you need additional information to answer a question.

    Args:
        query (str): The user's question or search query.

    Returns:
        List[Document]: A list of the top-ranked Document objects, limited to TOP_K (5) results.
    """
    retrieved_docs = retriever.invoke(query)
    # return retrieved_docs[:TOP_K]
    return retrieved_docs

@tool
def should_continue() -> None:
    """
    Use this tool if you determine that you have enough context to respond to the questions of the user.
    """
    return None

# Initialize language model
llm = ChatOllama(model="llama3-groq-tool-use:latest", temperature=0)

# Set up conversation inspector
inspect_conversation = inspect_conversation_template | llm.bind_tools(
    [retrieve_docs, should_continue], tool_choice="any"
)

# Set up response chain
response_chain = rag_template | llm

# TODO: Add support for the case of a problem answering a question, e.g.: 
# "I'm sorry but I do not have enough information to complete this task. 
# Can you provide more details or clarify your question?"
@custom_chain
async def chain(
    input: Dict[str, Any], **kwargs: Any
) -> AsyncIterator[OnToolEndEvent | OnChatModelStreamEvent]:
    """
    Implement a RAG QA chain with tool calls.

    This function is decorated with `custom_chain` to offer LangChain compatible
    astream_events, support for synchronous invocation through the `invoke` method,
    and OpenTelemetry tracing.
    """
    # Inspect conversation and determine next action
    inspection_result = inspect_conversation.invoke(input)

    log.info(f"Inspection result: {inspection_result.content}")

    tool_call_result = inspection_result.tool_calls[0]

    # Execute the appropriate tool based on the inspection result
    if tool_call_result["name"] == "retrieve_docs":
        # Retrieve relevant documents
        docs = retrieve_docs.invoke(tool_call_result["args"])
        # Format the retrieved documents
        formatted_docs = template_docs.format(docs=docs)
        # Create a ToolMessage with the formatted documents
        tool_message = ToolMessage(
            tool_call_id=tool_call_result["name"],
            name=tool_call_result["name"],
            content=formatted_docs,
            artifact=docs,
        )
    else:
        # If no documents need to be retrieved, continue with the conversation
        tool_message = should_continue.invoke(tool_call_result)

    # Update input messages with new information
    input["messages"] = input["messages"] + [inspection_result, tool_message]

    # Yield tool results metadata
    yield OnToolEndEvent(
        data={"input": tool_call_result["args"], "output": tool_message}
    )

    # Stream LLM response
    async for chunk in response_chain.astream(input=input):
        yield OnChatModelStreamEvent(data={"chunk": chunk})
