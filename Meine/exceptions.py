from textual.app import App

class InfoNotify(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ErrorNotify(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class WarningNotify(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message