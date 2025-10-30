import argparse

# Input Prompt
def input_prompt():
    parser = argparse.ArgumentParser(description='CLI LLM')
    parser.add_argument('prompt', type=str, help='The prompt to send to the LLM')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()
    return args.prompt, args.verbose
