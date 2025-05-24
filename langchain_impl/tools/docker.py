from langchain.tools import tool
import subprocess

@tool
def list_containers() -> str:
    """List all running Docker containers."""
    return subprocess.check_output(["docker", "ps"]).decode()

@tool
def list_all_containers() -> str:
    """List all Docker containers."""
    return subprocess.check_output(["docker", "ps","-a"]).decode()