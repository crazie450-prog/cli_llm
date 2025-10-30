import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file within the working directory. Creates the file if it doesn't exist, or overwrites it if it does.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file within the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    """
    Write content to a specified file within a working directory.
    
    Args:
        working_directory: The root directory that serves as a boundary
        file_path: Relative path to the file within the working_directory
        content: The content to write to the file as a string
    
    Returns:
        A success message or an error message
    """
    try:
        # Join the paths and get absolute paths
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Write the content to the file
        with open(abs_full_path, 'w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"