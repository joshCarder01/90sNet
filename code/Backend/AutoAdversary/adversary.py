import requests
import json
import time
import sys

# set flask server IP
FLASK_IP = "127.0.0.1:5000"
if len(sys.argv) > 1:
    FLASK_IP = sys.argv[1]


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


# when given an automated adversary action, it will find the index of the next step to check for (None if timeout not reached, -1 if all steps completed)
def get_last_setup_index(aaaction):
    setup_lst = aaaction['setup']
    t = time.time()
    # for each setup item, check its time, if not None, see if its reached timeout
    for i, setup_item in enumerate(setup_lst):
        if setup_item['time'] != None:
            continue
        if i == 0:
            return i
        if setup_lst[i-1]['timeout'] + setup_lst[i-1]['time'] > t:
            return None
        else:
            return i
    return -1


# Dict that holds all events to check for
event_checks = {
    "entrypoint_Crosley_0":{ #container name
        "AAAction1":{ #action name (anything unique)
            "setup":[ # setup steps (events to look for)
                {
                    "type":"file_mod", #event type
                    "keyword":"blueberry", #keyword in description
                    "time":None, # time event happens
                    "timeout":1, #timeout for waiting for next event to happen
                },
                {
                    "type":"file_mod",
                    "keyword":"raspberry",
                    "time":None,
                    "timeout":1,
                },
                ],
            "actions":[ # action steps (actions to take once all set up has been seen)
                {
                    "cmd":"cli",
                    "args":"exec -it entrypoint_Crosley_0 touch ISeeYou",
                    "delay":0, #delay for next action
                }
            ]
        },
        "ScoreRestartAction":{
            "setup": [
                {
                    "type": "score",
                    "keyword": None,
                    "time": None,
                    "timeout": 1
                }
            ],
            "actions": [
                {
                    "cmd": "cli",
                    "args": "restart entrypoint_Crosley_0"
                }
            ]
        }
    }
}

challengeset1=[
    'challengeset1_Baldwin_0',
    'challengeset1_Baldwin_1',
    'challengeset1_TUC_0',
    'challengeset1_TUC_1',
    'challengeset1_Manti_0',
    'challengeset1_Manti_1',
    'challengeset1_OldChem_0',
    'challengeset1_OldChem_1',
    'challengeset1_Reviechel_0',
    'challengeset1_Reviechel_1',
    'challengeset1_Zimmer_0',
    'challengeset1_Zimmer_1'
]

challengeset2= [
    'challengeset2_Baldwin_0',
    'challengeset2_Baldwin_1',
    'challengeset2_TUC_0',
    'challengeset2_TUC_1',
    'challengeset2_Manti_0',
    'challengeset2_Manti_1',
    'challengeset2_OldChem_0',
    'challengeset2_OldChem_1',
    'challengeset2_Reviechel_0',
    'challengeset2_Reviechel_1',
    'challengeset2_Zimmer_0',
    'challengeset2_Zimmer_1'
]

for i in challengeset1:
    event_checks[i] = {
        "ScoreRestartAction":{
            "setup": [
                {
                    "type": "score",
                    "time": None,
                    "timeout": 1
                }
            ],
            "actions": [
                {
                    "cmd": "cli",
                    "args": f"exec -t {i} bash -c echo -n '' > /score.txt"
                }
            ]
        }
    }

# Setup ChallengeSet2
for i in challengeset2:
    event_checks[i] = { #container name
        "AAAction1":{ #action name (anything unique)
            "setup":[ # setup steps (events to look for)
                {
                    "type":"cmd_changed_output", #event type
                    "keyword":"still logged in", #keyword in description
                    "time":None, # time event happens
                    "timeout":1, #timeout for waiting for next event to happen
                },
                ],
            "actions":[ # action steps (actions to take once all set up has been seen)
                {
                    "cmd":"cli",
                    "args": f"exec -it {i} /bin/sh -c /usr/lib/terminfo/a/ssh_adversary.sh",
                }
            ]
        },
        "ScoreRestartAction":{
            "setup": [
                {
                    "type": "score",
                    "time": None,
                    "timeout": 1
                }
            ],
            "actions": [
                {
                    "cmd": "cli",
                    "args": f"bash echo -n '' > /score.txt"
                }
            ]
        }
    }



last_time = time.time()
events = None

# While true, get list of events and evaluate each
while True:
    events, last_time = getEventsSince(last_time)
    for event in events:
        # go through each machine and action to see if applicable
        for machine_name, AAactions in event_checks.items():
            if event["machine_name"] != machine_name:
                continue
            for AAAName, AAaction in AAactions.items():
                i = get_last_setup_index(AAaction)
                if i == None or i == -1: #No settup steps either not ready or all already done
                    continue
                step = AAaction['setup'][i] #otherwise use this step
                
                # if event is right and keyword found in event description, 
                if step['type'] == event['type'] and True if step.get('keyword', None) is None else (step['keyword'] in event['description']):
                    print("step event {} found for {}".format(i, AAAName))
                    event_checks[machine_name][AAAName]['setup'][i]['time'] = time.time()
                if i == len(AAaction['setup']) - 1 and get_last_setup_index(AAaction) == -1:
                    print("take action")
                    for action in AAaction['actions']:
                        data = {}
                        data['cmd'] = action['cmd']
                        data['args'] = action['args'].split()
                        r = requests.post("http://{}/{}".format(FLASK_IP, "command"),
                            headers={'Content-Type':'application/json'},
                            json=data)
                        time.sleep(action.get('delay', 0))
                    continue
