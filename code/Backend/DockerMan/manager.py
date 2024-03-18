import subprocess
import time

def docker(command):
    return subprocess.Popen(['docker']+command.split(" "), stdout=subprocess.PIPE).stdout.read().decode()

while True:
    # get commands
    command_json = ""

    for cmd in command_json:
        # execute each command
        # return result
        pass
