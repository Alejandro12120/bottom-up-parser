from dataclasses import dataclass


@dataclass(slots=True)
class ParserError(Exception):
    message: str

    def __str__(self) -> str:
        """This method returns the parser error message.

        :returns: The parser error message
        """
        return self.message


class ErrorHandler:
    @staticmethod
    def raise_error(message: str) -> None:
        """This function raises a ParserError with the received message.

        :param message: The error message
        """
        raise ParserError(message)

    @staticmethod
    def format_error(error: Exception) -> str:
        """This function formats an exception as an error message.

        :param error: The exception to format
        :returns: The formatted error message
        """
        return f"ERROR: {error}"
