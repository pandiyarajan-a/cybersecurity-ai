import subprocess
from smolagent.tools import BaseTool

class MetasploitTool(BaseTool):
    name = "metasploit_scan"
    description = "Run Metasploit auxiliary scan via resource script."

    def run(self, resource_script: str = "resource/scan.rc") -> str:
        try:
            result = subprocess.run(
                ["msfconsole", "-q", "-r", resource_script],
                capture_output=True, text=True, timeout=120
            )
            return result.stdout
        except Exception as e:
            return f"Error running Metasploit: {str(e)}"