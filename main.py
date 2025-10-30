import os
from functions.input_prompt import input_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Hardcoded variables
model_name = "gemini-2.0-flash-001"
working_directory = None
system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def main():
    # Get user prompt and verbosity setting
    user_prompt, verbose = input_prompt()
        
    # Create message content for the LLM
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Generate response from the LLM
    response = client.models.generate_content(
        model = model_name,
        contents = messages,
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )
    
    # Output
    print(response.text)
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Calling function: {function_call.name}({function_call.args})")
    
    # Verbose output
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        



if __name__ == "__main__":
    main()
