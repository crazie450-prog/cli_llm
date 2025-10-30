import os

from config import MODEL_NAME, SYSTEM_PROMPT
from functions.input_prompt import input_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def main():
    # Get user prompt and verbosity setting
    user_prompt, verbose = input_prompt()

    # Verbose output - print user prompt first
    if verbose:
        print(f"User prompt: {user_prompt}")

    # Create message content for the LLM
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Generate response from the LLM
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[available_functions],
        ),
    )

    # Verbose output - print token counts
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Check if the response contains text
    if response.text:
        print(response.text)

    # Check all parts for function calls
    for part in response.candidates[0].content.parts:
        if part.function_call:
            function_call = part.function_call

            # Call the function using our call_function helper
            function_call_result = call_function(function_call, verbose=verbose)

            # Verify the result has the expected structure
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Function call did not return a valid response")

            # Print the result in verbose mode
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        



if __name__ == "__main__":
    main()
