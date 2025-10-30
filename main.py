import os
from utilities import input_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    # Get user prompt and verbosity setting
    user_prompt, verbose = input_prompt()
        
    # Create message content for the LLM
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Generate response from the LLM
    response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents = messages
    )
    
    # Output
    print(response.text)
    
    # Verbose output
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        



if __name__ == "__main__":
    main()
