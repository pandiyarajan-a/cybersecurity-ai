import datetime
import os
import yaml
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()
from tools import list_containers, list_all_containers, scan_image_trivy, run_nmap #, suggest_fixes

tools = [list_containers, list_all_containers, scan_image_trivy, run_nmap]
cs_llm = ChatOpenAI(model='gpt-4o')
cs_llm_with_tools = cs_llm.bind_tools(tools=tools)

from typing_extensions import TypedDict

class State(TypedDict):
    graph_state: str

from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

from typing import TypedDict, Annotated, List, Any, Optional

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def assistant(state: AgentState):

    sys_msg = SystemMessage(content=f"""You are cybersecurity expert, your name is Ashwin, an experienced penetration tester.
    Make use of the tools to perform tasks.""")

    return {"messages": [cs_llm_with_tools.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(state_schema=AgentState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()

# message = "List down all docker containers even if its in exited stage"
# # messages = [HumanMessage(content=message)]
# response = react_graph.invoke({"messages":message})
# print(response)
# print(response['messages'][-1].content)


def cs_agent(message, history):
    messages = {"messages":message}
    response = react_graph.invoke(messages)
    return response['messages'][-1].content

gr.ChatInterface(
    fn=cs_agent, 
    type="messages"
).launch()

