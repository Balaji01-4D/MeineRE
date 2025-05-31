class InfoNotify(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.severity = "error"
