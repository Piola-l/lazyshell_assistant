import re
import os

'''
Supported terminals:
gnome-terminal
ptyxis
'''

terminal = '/usr/bin/ptyxis'  # Используй терминал, который у тебя установлен

def parse(input_str: str, root_password: str, auto_execute_root: bool):
    commands = []
    matches = re.findall(r'([\$#])\s*(.*?)\s*[\$#]', input_str)  # Находим команды с префиксами $ или #

    for match in matches:
        prefix, command = match
        command = command.strip()

        if command:
            if prefix == "#":  # Если команда должна выполняться от рута
                if auto_execute_root:
                    command = f"echo '{root_password}' | sudo -S {command}"
                    print(command)
                else:
                    command = f"sudo {command}"

            commands.append(command)

    return commands

def execute(commands, execute: bool):
    for cmd in commands:
        if execute:
            match terminal[9:]:
                case "gnome-terminal":
                    os.system(f"gnome-terminal -- bash -c '{cmd}; exec bash'")  # Открываем команду в терминале
                case "ptyxis":
                    os.system(f"ptyxis -- bash -c '{cmd}; exec bash'")  # Открываем команду в терминале
