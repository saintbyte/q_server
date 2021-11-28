import threading
import time

from constants import TASK_CHANGE_LETTERS_COMMAND
from constants import TASK_REVERSE_COMMAND
from tasks import change_letters
from tasks import reserse


class Worker(threading.Thread):
    def __init__(self, working_queue):
        super().__init__()
        self.working_queue = working_queue

    def some_wait(self):
        time.sleep(1)

    def run(self):
        while True:
            new_task = self.working_queue.get_new_to_work()
            if not new_task:
                self.some_wait()
                continue
            result = ""
            if new_task["task"] == TASK_REVERSE_COMMAND:
                result = reserse(new_task["data"])
            if new_task["task"] == TASK_CHANGE_LETTERS_COMMAND:
                result = change_letters(new_task["data"])
            self.working_queue.set_result_by_task_id(new_task["task_id"], result)
            self.some_wait()
