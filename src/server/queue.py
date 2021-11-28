from multiprocessing import Lock

from constants import STATUS_COMPLETE
from constants import STATUS_NEW
from constants import STATUS_WORKING


class QServerTaskQueue:
    def __init__(self) -> None:
        self.lock = Lock()
        self.storage = []

    def get(self, key=None):
        if not len(self.storage):
            return

    def get_by_task_id(self, task_id):
        for item in self.storage:
            if item["task_id"] == task_id:
                return item

    def get_new(self):
        for item in self.storage:
            if item["status"] == STATUS_NEW:
                return item

    def get_new_to_work(self):
        self.lock.acquire()
        for index, item in enumerate(self.storage):
            if item["status"] == STATUS_NEW:
                self.storage[index]["status"] = STATUS_WORKING
                self.lock.release()
                return item
        self.lock.release()

    def set_result_by_task_id(self, task_id, result):
        self.lock.acquire()
        for index, item in enumerate(self.storage):
            if item["task_id"] == task_id:
                self.storage[index]["status"] = STATUS_COMPLETE
                self.storage[index]["result"] = result
                break
        self.lock.release()

    def put(self, data):
        data["status"] = STATUS_NEW
        self.lock.acquire()
        self.storage.append(data)
        self.lock.release()
