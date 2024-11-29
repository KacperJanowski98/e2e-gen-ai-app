from typing import Dict

from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode


# 1. Define tools
@tool
def search(query: str) -> str:
    """Simulates a web search. Use it get information on weather"""
    if "Wwa" in query.lower() or "Warsaw" in query.lower():
        return "It is 10 degrees and rainy"
    return "It's 15 degrees and sunny"

tools = [search]

# 2. Set up the language model
llm = ChatOllama(
    model="llama3-groq-tool-use:latest", temperature=0
).bind_tools(tools)

# 3. Define workflow components
def should_continue(state: MessagesState) -> str:
    """Determines whether to use tools or end the conversation."""
    last_message = state["messages"][-1]
    return "tools" if last_message.tool_calls else END

def call_model(state: MessagesState, config: RunnableConfig) -> Dict[str, BaseMessage]:
    """Calls the language model and returns the response."""
    system_message = "You are a helpful AI assistant."
    messages_with_system = [{"type": "system", "content": system_message}] + state[
        "messages"
    ]
    # Forward the RunnableConfig object to ensure the agent is capable of streaming the response.
    response = llm.invoke(messages_with_system, config)
    return {"messages": response}

# 4. Create the workflow graph
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))
workflow.set_entry_point("agent")

# 5. Define graph edges
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# 6. Compile the workflow
chain = workflow.compile()
