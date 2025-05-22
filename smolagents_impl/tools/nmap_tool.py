import subprocess
from smolagents.tools import BaseTool

class NmapTool(BaseTool):
    name = "nmap_scan"
    description = "Run a basic Nmap scan on a target IP."

    def run(self, target_ip: str) -> str:
        try:
            result = subprocess.run(
                ["nmap", "-sV", target_ip],
                capture_output=True, text=True, timeout=60
            )
            return result.stdout
        except Exception as e:
            return f"Error running Nmap: {str(e)}"