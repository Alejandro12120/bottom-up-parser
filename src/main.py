import sys

from components.error_handler import ErrorHandler, ParserError
from components.forest_builder import ForestBuilder
from components.grammar_manager import GrammarManager
from components.input_reader import InputReader
from components.output_formatter import OutputFormatter
from components.output_writer import OutputWriter
from components.parser_engine import ParserEngine
from models.parser.parser_state import ParserState

if __name__ == "__main__":
    writer = None
    try:
        input_reader = InputReader(sys.argv)
        input_reader.read_input()

        grammar_manager = GrammarManager(input_reader.grammar_text)
        writer = OutputWriter(input_reader.output_path)

        # Because forest_builder requires a ParserState, here we are going to initialize the initial step
        for word in input_reader.input_words:
            input_symbols = InputReader.process_string(word)

            # TODO: only initialise ParserEngine one time?
            engine = ParserEngine(
                grammar=grammar_manager.grammar,
                forest_builder=ForestBuilder(ParserState(
                    input_pos=0,
                    forest=[],
                    consumed=[],
                    remaining_input=list(input_symbols),
                    right_most_derivation_hist=[],
                )),
                output_writer=writer
            )

            result = engine.parse(input_symbols)
            if engine.step_counter > 0:
                writer.write()

            writer.write(OutputFormatter.format_result(result))
            writer.write("=" * 80)

        exit(0) # TODO: exit 0 if at least one word is rejected?
    except ParserError as error:
        print(ErrorHandler.format_error(error))
        exit(1)
    finally:
        if writer is not None:
            writer.close()

