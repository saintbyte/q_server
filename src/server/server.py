import socket

from client_thread import ClienThread
from constants import MAX_CONNECTION


class Server(object):
    def __init__(self, host, port, working_queue):
        self.host = host
        self.port = port
        self.working_queue = working_queue
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(MAX_CONNECTION)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            ClienThread(client, address, self.working_queue).start()
