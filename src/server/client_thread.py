import logging
import socket
import threading
import uuid

from constants import ALL_ALLOWED_REQUESTS
from constants import CREATE_TASK_REQUEST
from constants import GET_RESULT_REQUEST
from constants import GET_STATUS_REQUEST
from constants import NOT_FOUND_ASWER
from constants import RECEIVE_SIZE
from data_parser import DataParser
from response import Response

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
                    response = Response(data_parser)
                    if data_parser.request not in ALL_ALLOWED_REQUESTS:
                        self.client.send(
                            response.get_error_response("method not allowed")
                        )
                        return False
                    if data_parser.request == CREATE_TASK_REQUEST:
                        task_id = str(uuid.uuid4())
                        self.working_queue.put(
                            {
                                "task_id": task_id,
                                "task": data_parser.command,
                                "data": data_parser.data,
                            }
                        )
                        response.set_result(task_id)
                    if data_parser.request in [GET_RESULT_REQUEST, GET_RESULT_REQUEST]:
                        queue_record = self.working_queue.get_by_task_id(
                            data_parser.request_data
                        )
                        if not queue_record:
                            response.set_result(NOT_FOUND_ASWER)
                        if queue_record and data_parser.request == GET_RESULT_REQUEST:
                            response.set_result(
                                queue_record.get("result", NOT_FOUND_ASWER)
                            )
                        if queue_record and data_parser.request == GET_STATUS_REQUEST:
                            response.set_result(
                                queue_record.get("status", NOT_FOUND_ASWER)
                            )
                    self.client.send(response.get_response())
                else:
                    raise socket.error("Client disconnected")
            except socket.error as e:
                logger.error(e)
                return False

    def join(self):
        if self.client:
            self.client.close()
