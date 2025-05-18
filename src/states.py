from typing_extensions import TypedDict

from typing import TypedDict, Annotated, List, Any, Optional

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]