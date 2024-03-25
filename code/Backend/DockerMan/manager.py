import subprocess
import time
import requests
import json


FLASK_IP = "127.0.0.1:5000"

def docker(command):
    return subprocess.Popen(['docker']+command.split(" "), stdout=subprocess.PIPE).stdout.read().decode()

while True:
    cmd = requests.get("http://{}/command".format(FLASK_IP),headers={'Content-Type':'application/json'},json={}).text
    if cmd == 'null\n':
        time.sleep(1)
        continue
    print(cmd)
    print("---")
    cmd = json.loads(cmd)
    if cmd['cmd'] == 'cli':
        cmd_result = docker(" ".join(cmd['args']))
        print(cmd_result)
        print("---")
        t=requests.post("http://{}/command/results".format(FLASK_IP),headers={'Content-Type':'application/json'},json={'id':cmd['id'], 'result':cmd_result}).text
        print(t)
