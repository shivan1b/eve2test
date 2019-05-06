class UnidentifiedValueError(Exception):
    """Exception raised when the value to be used is unidentifie."""
    def __init__(self, message):
        self.message = message
