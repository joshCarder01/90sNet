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
    
    def send_and_receive_http(self, data):
        r = requests.get("{}:{}".format(self.ip_address, self.port_number), 
                         headers={'content-type':'application/json'},
                         data=data)
        print(r.text)
    
    # Shortcut for getting events since a time
    def getEventsSince(self, unix_time_code):
        # command struct
        event_command = {
            "command":"getEventsSince",
            "args":[float(unix_time_code)]
        }

        # send command and get events
        new_events = json.loads(self.send_and_receive_http(json.dumps(event_command)))
        # calculate time of last event
        time_last_event = unix_time_code
        if len(new_events) > 0:
            time_last_event = float(list(new_events)[-1]) # gets the time of the last event

        return new_events, time_last_event