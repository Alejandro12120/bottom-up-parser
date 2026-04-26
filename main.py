import sys

from components.error_handler import ErrorHandler, ParserError
from components.forest_builder import ForestBuilder
from components.grammar_manager import GrammarManager
from components.input_reader import InputReader
from components.output_formatter import OutputFormatter
from components.parser_engine import ParserEngine
from models.parser.parser_state import ParserState

if __name__ == "__main__":
    try:
        input_reader = InputReader(sys.argv)
        input_reader.read_input()

        grammar_manager = GrammarManager(input_reader.grammar_text)

        # Because forest_builder requires a ParserState, here we are going to initialize the initial step
        engine = ParserEngine(
            grammar=grammar_manager.grammar,
            forest_builder=ForestBuilder(ParserState(
                input_pos=0,
                forest=[],
                consumed=[],
                remaining_input=list(input_reader.input_symbols),
                right_most_derivation_hist=[],
            ))
        )

        result = engine.parse(input_reader.input_symbols)
        if engine.step_counter > 0:
            print()

        print(OutputFormatter.format_result(result))
        exit(0 if result.accepted else 1)
    except ParserError as error:
        print(ErrorHandler.format_error(error))
        exit(1)
