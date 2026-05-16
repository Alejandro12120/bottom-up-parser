from pathlib import Path

from components.error_handler import ErrorHandler


class InputReader:
    def __init__(self, argv: list[str]):
        """This method initializes the input reader with the CLI arguments.

        :param argv: The CLI arguments
        """
        self.__argv = argv
        self.__grammar_text: str = ""
        self.__output_path: str = ""
        self.__input_words: list[str] = []
        self.__detailed_output: bool = True


    def read_input(self):
        """This method reads and stores the grammar, words and output path from the CLI arguments."""
        if not (4 <= len(self.__argv) <= 5):
            ErrorHandler.raise_error("Expected at least 3 CLI parameters.")

        grammar_path, words_path, output_path = self.__argv[1], self.__argv[2], self.__argv[3]
        if len(self.__argv) == 5:
            self.__detailed_output = (self.__argv[4] == "True" or self.__argv[4] == "true")

        self.__grammar_text = InputReader.read_grammar_file(grammar_path)
        self.__output_path = output_path
        self.__input_words = InputReader.read_words_file(words_path)


    @property
    def grammar_text(self) -> str:
        """This method returns the grammar text.

        :returns: The grammar text
        """
        return self.__grammar_text

    @property
    def output_path(self) -> str:
        """This method returns the output path.

        :returns: The output path
        """
        return self.__output_path

    @property
    def input_words(self) -> list[str]:
        """This method returns the input words.

        :returns: A list of input words
        """
        return self.__input_words

    @property
    def detailed_output(self):
        """This method returns whether detailed parser output is enabled.

        :returns: True if detailed parser output is enabled, False if not
        """
        return self.__detailed_output

    @staticmethod
    def read_words_file(words_path: str) -> list[str]:
        """
        This function reads the words file and returns a list of strings split by $.

        :param words_path: The words file
        :return: A list of strings
        """

        path = Path(words_path)
        try:
            content = path.read_text(encoding="utf-8")
            content = content.replace("\n", "").replace("\r", "")

            if not content:
                ErrorHandler.raise_error("Words file is empty.")

            if not content.endswith("$"):
                ErrorHandler.raise_error("Words file must end with $.")

            words = content.split("$")[:-1]

            if any(word == "" for word in words):
                ErrorHandler.raise_error("Empty words are not supported.")

            return [word + "$" for word in words]
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
