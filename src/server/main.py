import logging
import os
from queue import QServerTaskQueue

from constants import DEFAULT_HOST
from constants import DEFAULT_PORT
from server import Server
from worker import Worker

logger = logging.getLogger(__name__)

RESULTS = []


if __name__ == "__main__":
    host = os.environ.get("HOST", DEFAULT_HOST)
    port_num = os.environ.get("PORT", DEFAULT_PORT)
    working_queue = QServerTaskQueue()
    try:
        port_num = int(port_num)
    except ValueError:
        logger.error("PORT not set or not number")
        quit()
    Worker(working_queue).start()
    Server(host, port_num, working_queue).listen()
