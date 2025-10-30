from functions.run_python_file import run_python_file


def main():
    # Test 1: Run calculator without arguments (should print usage instructions)
    print('Test 1: run_python_file("calculator", "main.py")')
    result = run_python_file("calculator", "main.py")
    print(result)
    print()

    # Test 2: Run calculator with arguments
    print('Test 2: run_python_file("calculator", "main.py", ["3 + 5"])')
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print()

    # Test 3: Run calculator tests
    print('Test 3: run_python_file("calculator", "tests.py")')
    result = run_python_file("calculator", "tests.py")
    print(result)
    print()

    # Test 4: Try to run file outside working directory (should error)
    print('Test 4: run_python_file("calculator", "../main.py")')
    result = run_python_file("calculator", "../main.py")
    print(result)
    print()

    # Test 5: Try to run non-existent file (should error)
    print('Test 5: run_python_file("calculator", "nonexistent.py")')
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print()

    # Test 6: Try to run non-Python file (should error)
    print('Test 6: run_python_file("calculator", "lorem.txt")')
    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print()


if __name__ == "__main__":
    main()