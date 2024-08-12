import sys
def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

def get_float(line_list):
    checklist = []
    for value in line_list:
        value = value.replace('[', '')
        value = value.replace(']', '')
        if is_float(value):
            continue
        else:
            if value[0].isdigit(): #loophole if number starts  at 0.1
                checklist.append(value)
            else:
                continue
    

    float_list = []
    for line in checklist:
        count  = 0
        line = line.split('.')
        new_str = ''
        new_list= []
        for number in range(len(line)):
            if number == 0:
                new_str += f"{line[number]}."
            elif number == 1:
                new_str += line[number]
            elif number == 2:
                new_list.append(new_str)
                new_list.append(".")
                new_list.append(line[number])
            else:
                new_list.append(".")
                new_list.append(line[number])

        if new_list[-1] == '':
            new_list.pop()
        
        float_list.extend(new_list)
        float_list.append(f'{is_float(checklist[count])}')
        new_str = ''
        new_list= []
        count +=1
    
    # if number is unparsable replace boolean False and part of the string is parsable
    for i in range(len(checklist)):
        replace = line_list.index(f"[{checklist[i]}]")
        line_list[replace:replace+1] = (float_list)
    
    for i in range(len(line_list)):
        line_list[i] = line_list[i].replace("[", "")
        line_list[i] = line_list[i].replace("]", "")


    return line_list

def check_numbers(line):
    new_string = ""
    ignore = False
    #putting ||| to digits 
    for i in range(len(line)):
        if ignore == True:
            if line[i] == ']':
                new_string += line[i]
                ignore = False
                continue
            else:
                new_string += line[i]
                continue
        elif line[i] == '[':
            new_string += line[i]
            ignore = True
        elif line[i].isdigit() or line[i] == '.': 
            new_string += f"||{line[i]}|"
        else:
            new_string += line[i]
            continue

    #combining digits and grouping them inside || 
    new_string = new_string.replace('|||', '')
    new_string = new_string.replace('||', '[')
    new_string = new_string.replace('|', ']')
    new_string = new_string.replace('].[', '.')
    #brute force
    new_string = new_string.replace('[..]', '..')
    new_string = new_string.replace('[...]', '...')
    new_string = new_string.replace('[....]', '....')
    return new_string

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
    line = check_numbers(line)
    new_string = ""
    ignore = False
    #putting [] to single tokens 
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

    return line_list

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
    
    # line = check_numbers(line)
    #putting brackets into multiple tokens 
    if len(string_list) == 0:
        line = encaps_multiple_tokens(line)
    else:
        for string in string_list:
            place = encaps_multiple_tokens(line).find("[]") + 1
            line = encaps_multiple_tokens(line)
            line = line[:place] + f"{string}" + line[place:]

    #check if there is integer or float

    #putting brackets into single tokens
    line_list = encaps_single_tokens(check_numbers(line))
    for i in range(len(line_list)):
        if line_list[i] == '["]':
            line_list[i] = line_list[i].replace('["]','[u]')
        elif line_list[i] == '[//]':
            line_list[i] = line_list[i].replace('[//]','[c]')
    
    return get_float(line_list)

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
        line = str(line)
        line_list = encaps_string(line)
        for i in range(len(line_list)):
            if line_list[i] == 'False':
                print("EOF  null")
                exit(0)
            elif line_list[i] == "c":
                break
            elif line_list[i] in interpreter_dict:
                print(f"{interpreter_dict.get(line_list[i])} {line_list[i]} null")
            elif line_list[i].startswith('"'):
                line_list[i] = line_list[i].replace('"', "")
                print(f"STRING \"{line_list[i]}\" {line_list[i]}")
            elif is_float(line_list[i]) == True:
                print(f"NUMBER {(line_list[i])} {float(line_list[i])}")
            elif line_list[i] == "u":
                error = True
                print(f'[line {line_count}] Error: Unterminated string.', file=sys.stderr,)
                break
            elif line_list[i] == "\t" or line_list[i] == " " or line_list[i] == "\n" or line_list[i] == "\r" or line_list[i] == "\0" or line_list[i] == '':
                continue
            else:
                error = True
                print(f'[line {line_count}] Error: Unexpected character: {line_list[i]}', file=sys.stderr,)
        line_count += 1
    print("EOF  null")

    if error:
        exit(65)
    else:
        exit(0)
    

if __name__ == "__main__":
    main()
