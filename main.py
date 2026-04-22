import sys

from components.input_reader import InputReader

if __name__ == "__main__":
    input_reader = InputReader(sys.argv)

    if not input_reader.read_input():
        # TODO: Handle error
        exit(1)
    
