import logging

from constants import NEW_LINE
from constants import REQUEST_LINES_COUNT
from constants import SPACE

logger = logging.getLogger(__name__)


class DataParser:
    def __init__(self, data):
        self.data = data.decode()
        self.data_not_complete = True
        self.request = ""
        self.command = ""
        self.request_data = ""
        self.parse()

    def is_complete(self):
        return not self.data_not_complete

    def append(self, data):
        self.data = self.data + data
        self.parse()

    def parse(self):
        if NEW_LINE not in self.data:
            return
        parsed_arr = self.data.split(NEW_LINE)
        if len(parsed_arr) <= REQUEST_LINES_COUNT:
            return
        self.data_not_complete = False
        self.request = parsed_arr[0].strip().upper()
        self.request_data = parsed_arr[1]
        if SPACE in parsed_arr[1]:
            second_line_arr = parsed_arr[1].split(SPACE)
            self.command = second_line_arr[0].strip().upper()
            self.request_data = second_line_arr[1].strip()
        return
