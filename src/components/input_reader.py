from pathlib import Path

from components.error_handler import ErrorHandler


class InputReader:
    def __init__(self, argv: list[str]):
        self.__argv = argv
        self.__grammar_text: str = ""
        self.__output_path: str = ""
        self.__input_words: list[str] = []

    def read_input(self):
        if len(self.__argv) != 4:
            ErrorHandler.raise_error("Expected 3 CLI parameters.")

        grammar_path, words_path, output_path = self.__argv[1], self.__argv[2], self.__argv[3]

        self.__grammar_text = InputReader.read_grammar_file(grammar_path)
        self.__output_path = output_path
        self.__input_words = InputReader.read_words_file(words_path)


    @property
    def grammar_text(self) -> str:
        return self.__grammar_text

    @property
    def input_words(self) -> list[str]:
        return self.__input_words

    @staticmethod
    def read_words_file(words_path: str) -> list[str]:
        """
        This function reads the words file and returns a list of strings split by $.

        :param words_path: The words file
        :return: A list of strings
        """

        path = Path(words_path)
        try:
            content = path.read_text(encoding='utf-8')
            if not content:
                ErrorHandler.raise_error("Words file is empty.")

            if not content.endswith("$"):
                ErrorHandler.raise_error("Words file msut end with $.")


            content = content.replace("\n", "").replace("\r", "")

            parts = content.split('$')

            if any(word == "" for word in parts):
                ErrorHandler.raise_error("Empty words are not supported.")

            return [word + '$' for word in parts[:-1]]
        except OSError as exc:
            ErrorHandler.raise_error(f"Unable to read words file: {path} ({exc.strerror})")
        raise AssertionError("unreachable")

    @staticmethod
    def process_string(string: str) -> list[str]:
        """This function processes the input string, checks if it ends with $ and returns a list of characters

        :param string: The input string
        :returns: The list of characters of the input string without $
        """
        if not string.endswith('$'):
            ErrorHandler.raise_error(f"The input string {string} does not end with $")

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
