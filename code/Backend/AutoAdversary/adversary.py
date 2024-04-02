import requests
import json
import time

FLASK_IP = "127.0.0.1:5000"

def getEventsSince(unix_time_code):
    command = "getEventsSince"
    data = {
        "time":float(unix_time_code)
    }
    new_events = json.loads(requests.get("http://{}/{}".format(FLASK_IP, command),
                        headers={'Content-Type':'application/json'},
                        json=data).text)

    # calculate time of last event
    time_last_event = unix_time_code
    if len(new_events) > 0:
        time_last_event = float(list(new_events)[-1]['time']) # gets the time of the last event

    return new_events, time_last_event

def get_last_setup_index(aaaction):
    setup_lst = aaaction['setup']
    t = time.time()

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

event_checks = {
    "proxy":{
        "AAAction1":{
            "setup":[
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
            "actions":[
                {
                    "cmd":"cli",
                    "args":"exec -it proxy touch ISeeYou",
                    "delay":0, #delay for next action
                }
            ]
        }
    }
}



last_time = time.time()
events = None
while True:
    events, last_time = getEventsSince(last_time)
    #print(events)
    #time.sleep(10)
    for event in events:
        for machine_name, AAactions in event_checks.items():
            if event["machine_name"] != machine_name:
                continue
            for AAAName, AAaction in AAactions.items():
                i = get_last_setup_index(AAaction)
                if i == None or i == -1:
                    continue
                step = AAaction['setup'][i]
                if step['type'] == event['type'] and step['keyword'] in event['description']:
                    print("found")
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
                        time.sleep(action['delay'])
                    continue
