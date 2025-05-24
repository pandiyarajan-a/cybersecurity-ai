from smolagents import CodeAgent, OpenAIServerModel, MultiStepAgent
import yaml, os
from  final_answer import FinalAnswerTool
from tools.vulnscan_tools import run_nmap, run_msf #, list_containers, list_all_containers, scan_image_trivy, 
from Gradio_UI import GradioUI

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from dotenv import load_dotenv

load_dotenv()

endpoint = "http://localhost:6006/v1/traces"
trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)

# Loading prompts
metasploit_prompt = ""
with open("smolagents_impl/prompts/metasploit_prompt.txt", 'r') as file:
    metasploit_prompt = file.read()

metasploit_prompt_template = ""
with open("smolagents_impl/prompts/metasploit_prompt.yaml", 'r') as stream:
    metasploit_prompt_template = yaml.safe_load(stream)

final_answer = FinalAnswerTool()

gpt_4o_model = OpenAIServerModel(
    model_id="gpt-4o"
)

# Qwen25_model = InferenceClientModel(
#     max_tokens=2096,
#     temperature=0.5,
#     model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
#     custom_role_conversions=None,
# )

vulnscan_agent = CodeAgent(
    model = gpt_4o_model,
    tools = [final_answer, run_nmap, run_msf], #, list_containers, list_all_containers, scan_image_trivy,],
    max_steps = 5,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None
)

# GradioUI(vulnscan_agent).launch()
message = metasploit_prompt + """ 
Target: `172.18.9.102`  
Use Case: `Check common open ports`
"""
message2 = metasploit_prompt + """ 
run a common port check on 172.18.9.102
"""
message3 =  metasploit_prompt + "Full reconnaissance scan on 172.18.9.102"


vulnscan_agent.run(message3)