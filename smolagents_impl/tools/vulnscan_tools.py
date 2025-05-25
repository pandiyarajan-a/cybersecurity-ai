from smolagents.tools import tool
import subprocess

# docker_client = from_env()

# @tool
# def list_containers() -> str:
#     """List all running Docker containers."""
#     return subprocess.check_output(["docker", "ps"]).decode()

# @tool
# def list_all_containers() -> str:
#     """List all Docker containers."""
#     return subprocess.check_output(["docker", "ps","-a"]).decode()

# @tool
# def scan_image_trivy(image: str) -> str:
#     """Scan a Docker image for vulnerabilities using Trivy.
#     Args:
#         image: variable holds the docker image name or id.
#     """
#     return subprocess.check_output(["trivy", "image", image]).decode()

@tool
def run_nmap(target_ip: str) -> str:
    """
    Executes an Nmap scan on the provided IP address.

    Args:
        target_ip (str): IP address of the target system.

    Returns:
        str: Output of the Nmap scan or error message.
    """
    try:
        result = subprocess.run(
            ["nmap", "-sV", target_ip],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout
    except Exception as e:
        return f"Error running Nmap: {str(e)}"

@tool
def run_msf(script_content: str) -> str:
    """
    Runs Metasploit using a provided .rc-style script as stdin.

    Args:
        script_content (str): Full content of the Metasploit script.

    Returns:
        str: Output of the Metasploit console or error message.
    """
    try:
        result = subprocess.run(
            ["msfconsole", "-q", "-r", "/dev/stdin"],
            input=script_content,
            text=True,
            capture_output=True,
            timeout=180
        )
        return result.stdout
    except Exception as e:
        return f"Error running Metasploit: {str(e)}"