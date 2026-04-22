import sys

from components.error_handler import ErrorHandler, ParserError
from components.input_reader import InputReader

if __name__ == "__main__":
    try:
        input_reader = InputReader(sys.argv)

        input_reader.read_input()

    except ParserError as error:
        print(ErrorHandler.format_error(error))
        exit(1)
