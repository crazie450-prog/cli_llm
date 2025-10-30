import os

def get_file_content(working_directory, file_path):
    """
    Retrieve the content of a specified file within a working directory.
    
    Args:
        working_directory: The root directory that serves as a boundary
        file_path: Relative path to the file within the working_directory
    
    Returns:
        The content of the file as a string or an error message
    """
    try:
        # Join the paths and get absolute paths
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)
        
        # Check if the path is within the working directory boundaries
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path is actually a file
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read and return the file content
        with open(abs_full_path, 'r') as file:
            content = file.read()
        
        return content
    
    except Exception as e:
        return f"Error: {str(e)}"