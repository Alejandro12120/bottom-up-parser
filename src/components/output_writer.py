from pathlib import Path

class OutputWriter:
    def __init__(self, output_path: str):
        """This method opens the output file where the parser will write its result.

        :param output_path: The output file path
        """
        self.__file = Path(output_path).open("w", encoding="utf-8")

    def write(self, text: str = ""):
        """This method writes a line in the output file and prints it.

        :param text: The text to write
        """
        print(text)
        self.__file.write(text + "\n")

    def close(self):
        """This method closes the output file."""
        self.__file.close()
