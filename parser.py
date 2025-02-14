import re
import os
import subprocess

# Supported terminals
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

def execute(commands, execute: bool, subprocess_terminal: bool):
    for cmd in commands:
        if execute:
            match terminal[9:]:
                case "gnome-terminal":
                    if subprocess_terminal:
                        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"])  # Open terminal as new task
                    else:
                        os.system(f"gnome-terminal -- bash -c '{cmd}; exec bash'")  # Open terminal
                case "ptyxis":
                    if subprocess_terminal:
                        subprocess.Popen([terminal, "--", "bash", "-c", f"{cmd}; exec bash"])  # Open terminal as new task
                    else:
                        os.system(f"{terminal} -- bash -c '{cmd}; exec bash'")  # Open terminal
