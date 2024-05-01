def print_commands(commands):
    string = ''

    for command in commands:
        if string:
            string += ' | '

        string += f"{command['key']}: {command['name']}"

    print(string)
