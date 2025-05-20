from smolagents import CodeAgent, InferenceClientModel, tool, OpenAIServerModel
import yaml
from  final_answer import FinalAnswerTool
from tools import list_containers, list_all_containers, scan_image_trivy, run_nmap
from Gradio_UI import GradioUI

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


endpoint = "http://localhost:6006/v1/traces"
trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)

with open("/home/vidhn/Projects/cybersecurity-ai/smolagent_framework/src/prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

final_answer = FinalAnswerTool()

# model = OpenAIServerModel(
#     model_id="gpt-4o",
#     api_key=os.environ['OPENAI_API_KEY']
# )

model = InferenceClientModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)

agent = CodeAgent(
    model = model,
    tools = [final_answer,list_containers, list_all_containers, scan_image_trivy, run_nmap],
    max_steps = 3,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates,
)

GradioUI(agent).launch()
# agent.run("List out all the running containers")