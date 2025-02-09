class InfoNotify(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.severity = "information"


class ErrorNotify(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.severity = "error"


class WarningNotify(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.severity = "warning"
