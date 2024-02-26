import socket, time
import threading
import json
import requests

class NetClient:

    def __init__(self, ip_address, port_number):
        self.ip_address = ip_address
        self.port_number = port_number

    def send_and_receive(self, data):
        # Set up connection
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.ip_address, self.port_number))
        # Send message
        server.send(bytes(data, 'utf-8'))
        # Get message
        r_data =  server.recv(2048).decode()
        server.close()
        return r_data
    
    def send_and_receive_http(self, command, data):
        r = requests.get("http://{}:{}/{}".format(self.ip_address, self.port_number, command),
                         headers={'Content-Type':'application/json'},
                         json=data)
        print("\n\n",r.text,"\n\n")
        return r.text
    
    # Shortcut for getting events since a time
    def getEventsSince(self, unix_time_code):
        # command struct
        event_command = {
            "time":float(unix_time_code)
        }

        # send command and get events
        
        new_events = json.loads(self.send_and_receive_http("getEventsSince", event_command))
        # calculate time of last event
        time_last_event = unix_time_code
        if len(new_events) > 0:
            time_last_event = float(list(new_events)[-1]['time']) # gets the time of the last event

        return new_events, time_last_event
    
    def http_command(self, cmd_str):
        cmd_dict = cmd_to_dict(cmd_str)
        command = cmd_dict['command']
        data = json.dumps(cmd_dict['options'])
        self.send_and_receive(command, data)
    

def cmd_to_dict(cmd_str):
    json_dict = {
        'command':None,
        'args':[],
        'options':{}
    }

    cmd_tokens = cmd_str.split(" ")
    json_dict['command'] = cmd_tokens[0]
    
    token_ptr = 1

    while token_ptr < len(cmd_tokens):
        token = cmd_tokens[token_ptr]
        if token.startswith("-") and not token.startswith("--"):
            for flag in token[1:]:
                json_dict['options'][flag] = True
        elif token.startswith("--"):
            json_dict['options'][token[2:]] = cmd_tokens[token_ptr + 1]
            token_ptr += 1
        else:
            json_dict['args'] += [token]
        token_ptr += 1

    return json_dict

def cmd_to_json(cmd_str):
    return json.dump(cmd_to_dict(cmd_str))