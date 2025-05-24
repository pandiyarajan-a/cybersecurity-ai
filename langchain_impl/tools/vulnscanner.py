from langchain.tools import tool
import subprocess


@tool
def scan_image_trivy(image: str) -> str:
    """Scan a Docker image for vulnerabilities using Trivy."""
    return subprocess.check_output(["trivy", "image", image]).decode()

@tool
def run_nmap(target_ip: str) -> str:
    """Executes an Nmap scan on the provided IP address."""
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
    """Runs Metasploit using a provided .rc-style script as stdin."""
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