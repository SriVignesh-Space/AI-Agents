import os
from collections.abc import Sequence
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import SecretStr

from .tools import tools

load_dotenv()

model = ChatOpenAI(
    base_url=os.environ.get("BASE_URL"),
    model=os.environ.get("MODEL", "sample"),
    api_key=SecretStr("my-secret-key"),
    temperature=0,
)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def model_call(state: AgentState) -> AgentState:
    model_with_tools = model.bind_tools(tools)
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def decision(state: AgentState):
    last_message = state["messages"][-1]  
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tool"
    return "user"


def user_input(state: AgentState) -> AgentState:
    if len(state["messages"]) > 2:
        message = input("Enter (exit/quit to close): ")
        return {"messages": [HumanMessage(content=message)]}
    return state


def user_input_check(state: AgentState):
    last_message = state["messages"][-1]
    if (
        isinstance(last_message, HumanMessage)
        and last_message.content == "exit"
        or last_message.content == "quit"
    ):
        return "end"
    return "continue"

def check_save(state : AgentState):
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage):
            if message.name == 'save':
                return "end"
            return "model_call"
    return "model_call"

graph = StateGraph(AgentState);

graph.add_node("user_input", user_input);
graph.add_node("model_call", model_call);
graph.add_node("tool_node", ToolNode(tools=tools))

graph.add_edge(START, "user_input");
graph.add_conditional_edges("user_input", user_input_check, {
    "continue" : "model_call",
    "end" : END
})

graph.add_conditional_edges("model_call", decision, {
    "user" : "user_input",
    "tool" : "tool_node",
})

graph.add_conditional_edges("tool_node", check_save, {
    "end" : END,
    "model_call" : "model_call"
})

app = graph.compile()
