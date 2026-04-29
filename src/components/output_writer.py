from pathlib import Path

class OutputWriter:
    def __init__(self, output_path: str):
        self.__file = Path(output_path).open("w", encoding="utf-8")

    def write(self, text: str = ""):
        print(text)
        self.__file.write(text + "\n")

    def close(self):
        self.__file.close()