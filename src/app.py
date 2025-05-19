
import gradio as gr
from dotenv import load_dotenv
load_dotenv()
from graph import GraphBuilder

# configure the Phoenix tracer
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
tracer_provider = register(
  project_name="cybersecurity-ai", # Default is 'default'
  auto_instrument=True # Auto-instrument your app based on installed OI dependencies
)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)


# Graph
graph_builder = GraphBuilder()
graph = graph_builder.build()


# message = "List down all docker containers even if its in exited stage"

# response = react_graph.invoke({"messages":message})
# print(response)
# print(response['messages'][-1].content)

def cs_agent(message, history):
    messages = {"messages":message}
    response = graph.invoke(messages)
    return response['messages'][-1].content

gr.ChatInterface(
    fn=cs_agent, 
    type="messages"
).launch()

