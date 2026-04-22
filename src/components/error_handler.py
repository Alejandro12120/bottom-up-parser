from dataclasses import dataclass


@dataclass(slots=True)
class ParserError(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


class ErrorHandler:
    @staticmethod
    def raise_error(message: str) -> None:
        raise ParserError(message)

    @staticmethod
    def format_error(error: Exception) -> str:
        return f"ERROR: {error}"
