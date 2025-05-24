from langchain_openai import ChatOpenAI
from tools.docker import list_containers, list_all_containers
from tools.vulnscanner import run_msf, run_nmap, scan_image_trivy

class VulnScanner:
    
    def __init__(self):
        self.brain = ChatOpenAI(model="gpt-4o")
        self.tools = [run_msf, run_nmap, scan_image_trivy, list_containers, list_all_containers]
        self.brain = self.brain.bind_tools(tools=self.tools)