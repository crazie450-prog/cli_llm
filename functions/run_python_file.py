import os
import subprocess
import sys
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory with a 30-second timeout. Captures stdout and stderr, and returns the output along with exit code information.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file (.py) within the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    """
    Execute a Python file within a specified working directory with security checks.

    Args:
        working_directory: The root directory that serves as a boundary
        file_path: Relative path to the Python file within the working_directory
        args: Optional list of command-line arguments to pass to the script

    Returns:
        A string containing the execution results or error message
    """
    try:
        # Join the paths and get absolute paths
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)

        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir + os.sep) and abs_full_path != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists
        if not os.path.exists(abs_full_path):
            return f'Error: File "{file_path}" not found.'

        # Check if the file is a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute the Python file
        command = [sys.executable, file_path] + args
        completed_process = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Format the output
        output_parts = []

        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")

        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")

        # Check if no output was produced
        if not output_parts:
            return "No output produced."

        # Join the output parts
        result = "\n".join(output_parts)

        # Add exit code information if non-zero
        if completed_process.returncode != 0:
            result += f"\nProcess exited with code {completed_process.returncode}"

        return result

    except Exception as e:
        return f"Error executing Python file: {e}"
