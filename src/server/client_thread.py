import logging
import socket
import threading

from constants import RECEIVE_SIZE
from data_parser import DataParser

logger = logging.getLogger(__name__)


class ClienThread(threading.Thread):
    def __init__(self, client, address, working_queue):
        super().__init__()
        self.client = client
        self.address = address
        self.working_queue = working_queue

    def run(self):
        while True:
            try:
                data = self.client.recv(RECEIVE_SIZE)
                if data:
                    data_parser = DataParser(data)
                    while not data_parser.is_complete():
                        print("not data_parser.is_complete()")
                        data = self.client.recv(RECEIVE_SIZE)
                        if data:
                            data_parser.append(data)
                    print(f"Request: {data_parser.request}")
                    print(f"Command: {data_parser.command}")
                    print(f"Data: {data_parser.request_data}")
                    self.client.send(data_parser.get_response())
                else:
                    raise socket.error("Client disconnected")
            except socket.error as e:
                logger.error(e)
                return False

    def join(self):
        if self.client:
            self.client.close()
