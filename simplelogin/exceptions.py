from typing import Optional

class SimpleLoginException(Exception):
    def __init__(self, message: Optional[str]) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message

class InvalidAPIKey(SimpleLoginException):
    pass

class MethodNotAllowed(SimpleLoginException):
    pass

class UnknowError(SimpleLoginException):
    pass

ERROR_MAP = {
    "Wrong api key": InvalidAPIKey("Invalid API key."),
    "Method not allowed": MethodNotAllowed("Method not allowed."),
    "Unknown error": UnknowError("Unknown error."),
}