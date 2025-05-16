from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

from tools import list_containers # scan_image_trivy, run_nmap, suggest_fixes

def create_graph():
    builder = StateGraph()
    builder.add_node("Agent", RunnableLambda(agent_executor()))
    builder.set_entry_point("Agent")
    builder.add_edge("Agent", END)
    return builder.compile()