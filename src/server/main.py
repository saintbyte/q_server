import logging
import os
from multiprocessing import Queue

from constants import DEFAULT_HOST
from constants import DEFAULT_PORT
from server import Server

logger = logging.getLogger(__name__)

RESULTS = []


if __name__ == "__main__":
    host = os.environ.get("HOST", DEFAULT_HOST)
    port_num = os.environ.get("PORT", DEFAULT_PORT)
    working_queue = Queue()
    try:
        port_num = int(port_num)
    except ValueError:
        logger.error("PORT not set or not number")
        quit()

    Server(host, port_num, working_queue).listen()
