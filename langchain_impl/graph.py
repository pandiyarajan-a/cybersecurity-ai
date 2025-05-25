from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage

from states import AgentState
from agents.vulnscanner_agent import VulnScanner
from prompts import Prompts

class GraphBuilder:

    def __init__(self):
        self.vuln_scanner = VulnScanner()
        self.prompts = Prompts()

    def build(self):
        builder = StateGraph(state_schema=AgentState)
        builder.add_node("assistant", self.vulnscanner_agent)
        builder.add_node("tools", ToolNode(self.vuln_scanner.tools))

        builder.add_edge(START, "assistant")
        builder.add_conditional_edges(
            "assistant",
            tools_condition,
        )
        builder.add_edge("tools", "assistant")
        graph = builder.compile()
        return graph

    def vulnscanner_agent(self, state: AgentState):
        # print("", self.prompts.get("vuln_scanner.system_prompt"))
        sys_msg = SystemMessage(
            content=self.prompts.get.vulnscan_agent.system_prompt
        )
        return {"messages": [self.vuln_scanner.brain.invoke([sys_msg] + state["messages"])]}
