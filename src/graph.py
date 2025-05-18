from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

from states import AgentState
from tools import list_containers, list_all_containers, scan_image_trivy, run_nmap #suggest_fixes

tools = [list_containers, list_all_containers, scan_image_trivy, run_nmap]

from states import AgentState
from langchain_core.messages import SystemMessage


def create_graph(cs_llm_with_tools):

    def assistant(state: AgentState):
        sys_msg = SystemMessage(content=f"""You are cybersecurity expert, your name is Ashwin, 
                                an experienced penetration tester.Make use of the tools to perform 
                                tasks.""")

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
    graph = builder.compile()
    return graph