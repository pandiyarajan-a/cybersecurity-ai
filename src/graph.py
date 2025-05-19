from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage

from states import AgentState
from agents.docker_security_agent import StaticAnalyst

class GraphBuilder:

    def __init__(self):
        # self.agents = {
        #     {"docker_agent": StaticAnalyst().add_tools()}
        # }
        self.static_analyst = StaticAnalyst()

    def build(self):
        builder = StateGraph(state_schema=AgentState)
        builder.add_node("assistant", self.docker_agent)
        builder.add_node("tools", ToolNode(self.static_analyst.tools))

        builder.add_edge(START, "assistant")
        builder.add_conditional_edges(
            "assistant",
            tools_condition,
        )
        builder.add_edge("tools", "assistant")
        graph = builder.compile()
        return graph

    def docker_agent(self, state: AgentState):
        sys_msg = SystemMessage(
            content=self.static_analyst.system_prompt
        )
        return {"messages": [self.static_analyst.brain.invoke([sys_msg] + state["messages"])]}
