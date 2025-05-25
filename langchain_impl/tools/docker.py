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

@tool
def run_docker_command(command: str)-> str:
    """
    Runs a Docker command using the command line.

    Args:
    - command (str): The Docker command to execute.

    Returns:
    - output (str): The standard output of the command.
    - error (str): The standard error of the command, if any.
    - exit_code (int): The exit code of the command.
    """
    try:
        # Run the provided Docker command as a subprocess
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Capture the output and error
        output, error = process.communicate()
        
        # Decode byte strings to UTF-8
        output = output.decode('utf-8')
        error = error.decode('utf-8')

        # Get the exit code
        exit_code = process.returncode

        return output, error, exit_code

    except Exception as e:
        return "", str(e), -1