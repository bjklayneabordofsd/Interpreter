import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Check if the correct number of arguments have been passed.
    # If not, print usage instructions and exit the program.
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    # Assign the first argument (after script name) to 'command'.
    # This should be the operation to perform, e.g., "tokenize".
    command = sys.argv[1]

    # Assign the second argument to 'filename', which is expected to be the file to process.
    filename = sys.argv[2]

    # Check if the specified command matches the expected operation ("tokenize").
    # If not, print an error message and exit the program.
    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Open the specified file and read its contents into 'file_contents'.
    # if file_contents:
    #     raise NotImplementedError("Scanner not implemented")
    # else:
        # If the file is empty, print a placeholder message indicating EOF (End Of File).
        # This line should be removed once the scanner is fully implemented.
        # print("EOF  null")

    for c in file_contents:
        if c == "(":
            print(f'LEFT_PAREN ( null')
        if c == ")":
            print(f'RIGHT_PAREN ) null')
        if c == "{":
            print(f'LEFT_BRACE {{ null')
        if c == "}":
            print(f'RIGHT_BRACE }} null')
        if c == "*":
            print(f'STAR * null')
        if c == ".":
            print(f'DOT . null')
        if c == ",":
            print(f'COMMA , null')
        if c == "+":
            print(f'PLUS + null')
        if c == "-":
            print(f'MINUS - null')
        if c == ";":
            print(f'SEMICOLON ; null')
    print("EOF  null")



if __name__ == "__main__":
    main()
