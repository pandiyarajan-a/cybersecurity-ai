from langchain.tools import tool
from docker import from_env
import subprocess
import docker

docker_client = from_env()

@tool
def list_containers() -> str:
    """List all running Docker containers."""
    return subprocess.check_output(["docker", "ps"]).decode()

@tool
def list_all_containers() -> str:
    """List all Docker containers."""
    return subprocess.check_output(["docker", "ps","-a"]).decode()

@tool
def scan_image_trivy(image: str) -> str:
    """Scan a Docker image for vulnerabilities using Trivy."""
    return subprocess.check_output(["trivy", "image", image]).decode()

@tool
def run_nmap(container_id: str, ports: str = "1-65535") -> str:
    """Run Nmap port scan against a container's exposed ports."""
    ip = docker_client.containers.get(container_id).attrs['NetworkSettings']['IPAddress']
    return subprocess.check_output(["nmap", "-p", ports, ip]).decode()