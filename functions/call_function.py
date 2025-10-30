from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Mapping of function names to actual function references
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False):
    """
    Handle the abstract task of calling one of our four functions.

    Args:
        function_call_part: A types.FunctionCall with .name and .args properties
        verbose: If True, print detailed information about the function call

    Returns:
        A types.Content object with the function response
    """
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)

    # Print function call information
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check if the function exists
    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Add the working directory argument
    function_args["working_directory"] = "./calculator"

    # Call the function
    try:
        function = FUNCTION_MAP[function_name]
        function_result = function(**function_args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error calling function: {str(e)}"},
                )
            ],
        )
