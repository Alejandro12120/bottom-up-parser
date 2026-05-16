from components.forest_builder import ForestBuilder
from components.output_formatter import OutputFormatter
from components.output_writer import OutputWriter
from models.grammar.grammar import Grammar
from models.parser.backtrack_frame import BacktrackFrame
from models.parser.match import Match
from models.parser.parse_result import ParseResult
from models.parser.parser_state import ParserState


class ParserEngine:

    def __init__(self, grammar: Grammar, forest_builder: ForestBuilder, output_writer: OutputWriter, detailed_output: bool):
        """This method initializes the parser engine.

        :param grammar: The grammar used by the parser
        :param forest_builder: The forest builder used to update parser states
        :param output_writer: The output writer used to write parser steps
        :param detailed_output: True if the parser should print each step
        """
        self.__grammar = grammar
        self.__forest_builder = forest_builder
        self.__output_writer = output_writer
        self.__detailed_output = detailed_output
        self.__step_counter = 0
        self.__input_symbols: list[str] = []

    def parse(self, input_symbols: list[str]) -> ParseResult:
        """This is the core method, it invokes the parser, it receives the input symbols and returns a ParseResult object

        :param input_symbols: The input symbols of the string that it should parse
        :returns: A ParseResult object
        """
        self.__step_counter = 0
        self.__input_symbols = list(input_symbols)

        self.__forest_builder.state.build_full_forest()

        initial_state = self.__forest_builder.state.clone()

        # Instead of a while with a backtrack stack we are going to implement the backtrack via recursion
        # Therefore the backtrack stack will be the call stack of Python

        final_state = self.__search(initial_state)
        if final_state is None:
            return ParseResult(
                accepted=False,
                final_state=initial_state,
                final_root=None
            )

        final_root = final_state.consumed[0].clone()
        return ParseResult(
            accepted=True,
            final_state=final_state,
            final_root=final_root
        )

    def __search(self, state: ParserState) -> ParserState | None:
        """This is the recursion function, it uses the call stack of Python as backtrack stack.
        It receives a state and returns the final state or None if not.

        :param state: A ParserState object
        :returns: The final state as a ParserState object or none if it is not a final state.
        """
        # Stop condition
        if state.is_accepted(self.__grammar, self.__input_symbols):
            return state

        matches = self.__find_matches(state)
        if matches:
            # We save the remaining alternatives
            base_state = state.clone()
            frame = BacktrackFrame(state=base_state.clone(), alternatives=matches[1:])

            for match_index, match in enumerate(matches):
                candidate_state = frame.state.clone()

                self.__forest_builder.state = candidate_state
                self.__forest_builder.apply_reduction(match)

                self.__step_counter += 1
                if self.__detailed_output:
                    self.__output_writer.write(OutputFormatter.record_step(
                        step_number=self.__step_counter,
                        action="REDUCE",
                        state=candidate_state,
                        production=match.production.format()
                    ))
                    self.__output_writer.write()

                # We apply recursion
                result = self.__search(candidate_state)
                if result is not None:
                    return result

                # If the result is None, we have to backtrack
                restored_state = base_state.clone()
                self.__forest_builder.state = restored_state

                self.__step_counter += 1
                if self.__detailed_output:
                    self.__output_writer.write(OutputFormatter.record_step(
                        step_number=self.__step_counter,
                        action="BACKTRACK",
                        state=restored_state,
                        undo=match.production.format(),
                    ))
                    self.__output_writer.write()

                # if match_index < len(matches) - 1:
                #     frame.alternatives = matches[match_index + 1:]

            # If we have no matches left, we shift a symbol
            if state.remaining_input:
                shifted_state = base_state.clone()
                symbol = state.remaining_input[0]

                self.__forest_builder.state = shifted_state
                self.__forest_builder.apply_shift(symbol)

                self.__step_counter += 1
                if self.__detailed_output:
                    self.__output_writer.write(OutputFormatter.record_step(
                        step_number=self.__step_counter,
                        action="SHIFT",
                        state=shifted_state,
                        symbol=symbol,
                    ))
                    self.__output_writer.write()

                return self.__search(shifted_state)

        if state.remaining_input:
            shifted_state = state.clone()
            symbol = state.remaining_input[0]

            self.__forest_builder.state = shifted_state
            self.__forest_builder.apply_shift(symbol)

            self.__step_counter += 1
            if self.__detailed_output:
                self.__output_writer.write(OutputFormatter.record_step(
                    step_number=self.__step_counter,
                    action="SHIFT",
                    state=shifted_state,
                    symbol=symbol,
                ))
                self.__output_writer.write()

            return self.__search(shifted_state)
        return None

    def __find_matches(self, state: ParserState) -> list[Match]:
        """This method finds all the possible matches in a specific ParserState, and returns a list.

        :param state: A ParserState object
        :returns: The list of possible matches
        """
        matches: list[Match] = []
        working_symbols = [node.symbol for node in state.consumed]

        # We have to check if between all possible slices in the working symbols there is a match
        # between the slice and the right part of a production

        # working_part is the same as state.consumed
        # state.consumed = [S/2, A/4, a]
        # working_part = "SAa"

        for start_index in range(len(working_symbols)):
            # For each start_index, we get every possible and valid end_index
            # based on the length of the right side of each production
            for production in self.__grammar.productions:
                end_index = start_index + len(production.right_side)

                if end_index > len(state.consumed):
                    continue

                if working_symbols[start_index:end_index] == production.right_side:
                    matches.append(
                        Match(
                            production=production,
                            start_index=start_index,
                            end_index=end_index
                        )
                    )
        return matches

    @property
    def step_counter(self):
        """This method returns the number of parser steps.

        :returns: The number of parser steps
        """
        return self.__step_counter
#
#    @property
#    def forest_builder(self):
#        return self.__forest_builder
#
#    @forest_builder.setter
#    def forest_builder(self, forest_builder: ForestBuilder):
#        self.__forest_builder = forest_builder
