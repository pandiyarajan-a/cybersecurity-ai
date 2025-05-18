import datetime
import os
import yaml
import gradio as gr
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()


# configure the Phoenix tracer
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
tracer_provider = register(
  project_name="cybersecurity-ai", # Default is 'default'
  auto_instrument=True # Auto-instrument your app based on installed OI dependencies
)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

from tools import list_containers, list_all_containers, scan_image_trivy, run_nmap #, suggest_fixes
from graph import create_graph

tools = [list_containers, list_all_containers, scan_image_trivy, run_nmap]
cs_llm = ChatOpenAI(model='gpt-4o')
cs_llm_with_tools = cs_llm.bind_tools(tools=tools)

# Get graph
react_graph = create_graph(cs_llm_with_tools)

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

