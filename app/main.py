import sys

def string_to_list(line_list):
    for i in range(len(line_list)):
        if line_list[i] == "[//]":
            line_list[i] = line_list[i].replace('[//]', "[c]")
        elif line_list[i] == '["]':
            line_list[i] = line_list[i].replace('["]', "[u]")

    for i in range(len(line_list)):
        line_list[i] = line_list[i].replace("[", "")
        line_list[i] = line_list[i].replace("]", "")

    return line_list

def encaps_single_tokens(line):
    new_string = ""
    ignore = False
    for i in range(len(line)):
        if ignore == True:
            if line[i] == "]":
                new_string += line[i]
                ignore = False
            else:
                new_string += line[i]
        elif line[i] == "[":
            new_string += line[i]
            ignore = True
        else:
            new_string += f"[{line[i]}]"

    new_string = new_string.replace('][', "]][[")

    line_list = list(new_string.split(']['))

    return string_to_list(line_list)

# encapsulates all multiple tokens
def encaps_multiple_tokens(line):
    multiple_token = [ 
        "!=",
        ">=", 
        "<=",
        "==",
        "//",
    ]

    for token in multiple_token:
        line = line.replace(token, f"[{token}]")
    
    line = line.replace("[[", "[")
    line = line.replace("]]", "]")
    
    return line

#encapsulate all strings ("") in a bracket ([])
def encaps_string(line):
    #get coordinates of strings
    position_list = [i for i in range(len(line)) if line.startswith("\"", i)]
    string_list = []

    #store strings in string_list
    if len(position_list) > 1:
        for i in range(0, (len(position_list)//2) * 2, 2):
            string_list.append(line[position_list[i]:position_list[i+1]+1])
    else:
        pass
    
    #puting brackets into string using replace
    for i in range(len(string_list)):
        line = line.replace(string_list[i], f"[]")
    
    #putting brackets into multiple tokens 
    if len(string_list) == 0:
        line = encaps_multiple_tokens(line)
    else:
        for string in string_list:
            place = encaps_multiple_tokens(line).find("[]") + 1
            line = encaps_multiple_tokens(line)
            line = line[:place] + f"{string}" + line[place:]

    #putting brackets into single tokens
    line = encaps_single_tokens(line)

    return line

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_lines = file.readlines()

    # if file_contents:
    #     raise NotImplementedError("Scanner not implemented")
    # else:
    #     print("EOF  null") # Placeholder, remove this line when implementing the scanner

    interpreter_dict = {
        "(" : 'LEFT_PAREN',
        ")" : 'RIGHT_PAREN',
        "{" : 'LEFT_BRACE',
        "}" : 'RIGHT_BRACE',
        "*" : 'STAR',
        "." : 'DOT',
        "," : 'COMMA',
        "+" : 'PLUS',
        "-" : 'MINUS',
        ";" : 'SEMICOLON',
        "==" : 'EQUAL_EQUAL',
        "=" : "EQUAL",
        "!=" : 'BANG_EQUAL',
        "!" : 'BANG',
        ">=" : 'GREATER_EQUAL',
        ">" : 'GREATER',
        "<=" : 'LESS_EQUAL',
        "<" : 'LESS',
        "/" : 'SLASH',
    }


    error = False
    line_count = 1
    for line in file_lines:
        line = line.replace("<|TAB|>", "\t")
        line = line.replace("<|SPACE|>", " ")
        for token in encaps_string(line):
            if token == "c":
                break
            elif token in interpreter_dict:
                print(f"{interpreter_dict.get(token)} {token} null")
            elif token.startswith('"'):
                token = token.replace('"', "")
                print(f"STRING \"{token}\" {token}")
            elif token == "u":
                error = True
                print(f'[line {line_count}] Error: Unterminated string.', file=sys.stderr,)
                break
            elif token == "\t" or token == " " or token == "\n" or token == "\r" or token == "\0" or token == '':
                continue
            else:
                error = True
                print(f'[line {line_count}] Error: Unexpected character: {token}', file=sys.stderr,)
        line_count += 1
    print("EOF  null")

    if error:
        exit(65)
    else:
        exit(0)
    

if __name__ == "__main__":
    main()
