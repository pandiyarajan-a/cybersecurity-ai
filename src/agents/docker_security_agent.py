from langchain_openai import ChatOpenAI
from tools.docker_cs_test import list_containers, list_all_containers, scan_image_trivy
from states import AgentState
from langchain_core.messages import SystemMessage

class StaticAnalyst:

    def __init__(self):
        self.brain = ChatOpenAI(model="gpt-4o")
        self.tools = [list_containers, list_all_containers, scan_image_trivy]
        self.system_prompt = f"""You are cybersecurity expert, your name is Ashwin, 
                                an experienced penetration tester.Make use of the tools to perform 
                                tasks."""
        self.brain = self.brain.bind_tools(tools=self.tools)
        
        



    


