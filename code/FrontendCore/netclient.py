import socket, time
import threading

class NetClient:

    def __init__(self, ip_address, port_number):
        self.ip_address = ip_address
        self.port_number = port_number
        self.event_list = []

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
