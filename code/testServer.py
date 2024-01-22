import socket
import time
import json
import threading

# Handles only events
class EventManager:

    def __init__(self):
        self.events = {}
        self.external_commands = {
            "getEventsSince":{"args":["unix_time_stamp"], "func":self.get_events_since},
            "foo":{"args":["unix_time_stamp"], "func":self.get_events_since}
        }

    def add_event(self, event):
        self.events[time.time()] = event

    def get_events_since(self, unix_time_stamp):
        return_events = {}
        for key, val in self.events.items():
            if key > unix_time_stamp:
                return_events[key] = val
        return json.dumps(return_events)


# Handles incoming commands from client. Talks to event manager (and others) to execute commands and fulfill requests
class BackendManager:

    def __init__(self, **kwargs):
        self.managers = []
        self.managers += [kwargs["event_manager"]]
        # add other managers as needed

        self.all_commands = {}
        for manager in self.managers:
            self.all_commands |= manager.external_commands

        print(self.all_commands)

    def fulfill_request(self, cmd_json):
        cmd_dict = json.loads(cmd_json)
        if cmd_dict['command'] in self.all_commands:
            return self.all_commands[cmd_dict['command']]['func'](*cmd_dict['args'])
        else:
            return "commandNotFound"



# Networking boilerplate for accepting connection requests. Server loop references outside function to deal with io
class SocketServer:

    def __init__(self, ip_address, port_number):

        # config ip and port
        if ip_address == 'localhost':
            self.ip_address = '127.0.0.1'
        else:
            self.ip_address = ip_address
        self.port_number = port_number

        # bind socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port_number))

    def connect(self, handle_function):
        self.socket.listen()
        connection, ip_address = self.socket.accept()
        data = connection.recv(1024).decode()
        print("[{}]: {}".format(ip_address, data))
        output = handle_function(data)
        connection.sendall(output.encode())
        connection.close()

    # This should be used in its own thread so that other things can happen on the server at once
    def server_loop(self, handle_function):
        while True:
            self.connect(handle_function)

# Test function that will return the data within a larger string
def hello_world(data):
    return "hello [{}] world".format(data)


SS = SocketServer('localhost',9000)
EM = EventManager()
BM = BackendManager(event_manager = EM)

server_thread = threading.Thread(target=SS.server_loop, args=[BM.fulfill_request])
server_thread.start()

while True:
    event = input()
    EM.add_event(event)