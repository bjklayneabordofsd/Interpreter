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
        file_lines = file.readlines()

    # Open the specified file and read its contents into 'file_contents'.
    # if file_contents:
    #     raise NotImplementedError("Scanner not implemented")
    # else:
        # If the file is empty, print a placeholder message indicating EOF (End Of File).
        # This line should be removed once the scanner is fully implemented.
        # print("EOF  null")

    interpreter_dict = {
        "(" : 'LEFT_PAREN ( null',
        ")" : 'RIGHT_PAREN ) null',
        "{" : 'LEFT_BRACE { null',
        "}" : 'RIGHT_BRACE } null',
        "*" : 'STAR * null',
        "." : 'DOT . null',
        "," : 'COMMA , null',
        "+" : 'PLUS + null',
        "-" : 'MINUS - null',
        ";" : 'SEMICOLON ; null',
        "x" : 'EQUAL_EQUAL == null',
        "=" : "EQUAL = null",
        "b" : 'BANG_EQUAL != null',
        "!" : 'BANG ! null',
        "g" : 'GREATER_EQUAL >= null',
        ">" : 'GREATER > null',
        "l" : 'LESS_EQUAL <= null',
        "<" : 'LESS < null',
        "/" : 'SLASH / null',
    }

    error = False
    line_count = 1
    for line in file_lines:
        line_list = line.replace('!=', 'b').replace('>=', 'g').replace('<=', 'l').replace('==', 'x').replace('//', 'c').replace('<|TAB|>', 's').replace('<|SPACE|>', 's')
        for c in line_list.strip():
            if c in interpreter_dict:
                print(interpreter_dict.get(c))
            elif c == "s" or c == " " or c == "\t":
                pass
            elif c == "c":
                break
            else:
                error = True
                print(f'[line {line_count}] Error: Unexpected character: {c}', file=sys.stderr,)
        line_count += 1
    print("EOF  null")

    if error:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
