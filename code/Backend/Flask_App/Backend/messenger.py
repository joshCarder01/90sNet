import socket
import time
import json
import logging


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
        logging.info("[{}]: {}".format(ip_address, data))
        output = handle_function(data)
        connection.sendall(output.encode())
        connection.close()
