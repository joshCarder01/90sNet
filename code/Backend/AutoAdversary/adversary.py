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
    pass

event_checks = {
    "proxy":{
        "AAAction1":{
            "setup":[
                {
                    "type":"file_mod", #event type
                    "keyword":"blueberry", #keyword in description
                    "time":None, # time event happens
                    "timeout":30, #timeout for waiting for next event to happen
                },
                {
                    "type":"file_mod",
                    "keyword":"raspberry",
                    "time":None,
                    "timeout":30,
                },
                ],
            "actions":[
                {
                    "cmd":"cli",
                    "args":"exec -it proxy wall I see you",
                    "delay":0, #delay for next action
                }
            ]
        }
    }
}



last_time = 0
events = None
while True:
    events, last_time = getEventsSince(last_time)
    #print(events)
    #time.sleep(10)
    for event in events:
        for machine_name, AAactions in event_checks.items():
            if event["machine_name"] != machine_name:
                continue
            for AAaction in AAactions:
                print(AAaction)