class Response:
    def __init__(self, data_parser):
        self.data_parser = data_parser
        self.result = "111"

    def set_result(self, result):
        self.result = result

    def get_error_response(self, error_message):
        return f"ERROR: {error_message}".encode()

    def get_response(self):
        return self.result.encode()
