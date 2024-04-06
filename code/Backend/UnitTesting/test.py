import subprocess
import time
import json
import requests

'''
These are basic tests to run against parts of the 90s net infrastructure using written defaults. Only run these tests when all other systems have been started. This also assumes a single system test
'''

test_machine_name = "proxy_Crosley_10.46.47.196"
FLASK_IP = "127.0.0.1:5000"

# gets a list of events from flask server since time argument
def getEventsSince(unix_time_code):
    # command formatting
    command = "getEventsSince"
    data = {
        "time":float(unix_time_code)
    }
    # request
    new_events = json.loads(requests.get("http://{}/{}".format(FLASK_IP, command),
                        headers={'Content-Type':'application/json'},
                        json=data).text)

    # calculate time of last event
    time_last_event = unix_time_code
    if len(new_events) > 0:
        time_last_event = float(list(new_events)[-1]['time']) # gets the time of the last event

    return new_events, time_last_event


def connect_docker(use_time):
    command = "exec -it {} echo foo".format(test_machine_name)
    result = subprocess.Popen(['docker']+command.split(" "), stdout=subprocess.PIPE).stdout.read().decode()
    return result == "foo\r\n"


def monitor_dir(use_time):
    # rm any old file
    command = 'docker exec -it {} rm bar.txt'.format(test_machine_name)
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    time.sleep(5)
    # write new file
    command = 'docker exec -it {} sh -c "echo foo > bar.txt"'.format(test_machine_name)
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    time.sleep(5)
    new_events, time_last_event = getEventsSince(use_time)
    return 'bar' in new_events[-1]['description']


def monitor_file(use_time):
    # rm any old file
    command = 'docker exec -it {} sh -c "echo NONE > hello_world.txt"'.format(test_machine_name)
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    time.sleep(5)
    # write new file
    command = 'docker exec -it {} sh -c "echo bar > hello_world.txt"'.format(test_machine_name)
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    time.sleep(5)
    new_events, time_last_event = getEventsSince(use_time)
    return 'bar' in new_events[-1]['description']


def manager_reply(use_time):
    data = {}
    data['cmd'] = "cli"
    data['args'] = "--version".split()
    r = requests.post("http://{}/{}".format(FLASK_IP, "command"),
        headers={'Content-Type':'application/json'},
        json=data)
    request_id = json.loads(r.text)
    while True:
        # waiting for result from server
        cmd_result = requests.get("http://{}/{}".format(FLASK_IP, "command/results"),
            headers={'Content-Type':'application/json'},
            json=request_id).text
        if str(request_id['id']) in cmd_result:
            cmd_result = json.loads(cmd_result)
            if cmd_result['id'] == request_id['id']:
                return True


def adversary_action(use_time):
    # rm any old file
    command = 'docker exec -it {} sh -c "echo blueberry > hello_world.txt"'.format(test_machine_name)
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    time.sleep(5)
    # write new file
    command = 'docker exec -it {} sh -c "echo raspberry > hello_world.txt"'.format(test_machine_name)
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    time.sleep(5)
    # check to see if new file exists
    command = 'docker exec -it {} ls'.format(test_machine_name)
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    return "ISeeYou" in result

    

functions_to_test = [
    connect_docker,
    monitor_dir,
    monitor_file,
    manager_reply,
    adversary_action,
]

for func in functions_to_test:
    result = func(time.time())
    if result == True:
        print("{}\t\t[PASS]".format(func.__name__))
    else:
        print("{}\t\t[FAIL]".format(func.__name__))