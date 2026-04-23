from pathlib import Path

from components.error_handler import ErrorHandler


class InputReader:
    def __init__(self, argv: list[str]):
        self.__argv = argv
        self.__grammar_text: str = ""
        self.__input_symbols: list[str] = []

    def read_input(self):
        if len(self.__argv) != 3:
            ErrorHandler.raise_error("Expected 2 CLI parameters")

        grammar_path, string = self.__argv[1], self.__argv[2]

        self.__input_symbols = InputReader.process_string(string)
        self.__grammar_text = InputReader.read_grammar_file(grammar_path)


    @property
    def grammar_text(self) -> str:
        return self.__grammar_text

    @property
    def input_symbols(self) -> list[str]:
        return self.__input_symbols

    @staticmethod
    def process_string(string: str) -> list[str]:
        """This function processes the input string, checks if it ends with $ and returns a list of characters

        :param string: The input string
        :returns: The list of characters of the input string without $
        """
        if not string.endswith('$'):
            ErrorHandler.raise_error("The input string does not end with $")
            return []

        return list(string[:-1])

    @staticmethod
    def read_grammar_file(grammar_path: str) -> str:
        """This function opens the grammar file and returns the whole content.

        :param grammar_path: The path of the grammar file
        :returns: The contents of the file

        """

        path = Path(grammar_path)
        try:
            return path.read_text(encoding='utf-8')
        except OSError as exc:
            ErrorHandler.raise_error(f"Unable to read grammar file: {path} ({exc.strerror})")
        raise AssertionError("unreachable")
