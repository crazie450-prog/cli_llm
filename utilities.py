import sys

# Input Prompt
def input_prompt():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)
