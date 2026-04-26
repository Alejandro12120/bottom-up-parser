from components.forest_builder import ForestBuilder
from components.output_formatter import OutputFormatter
from models.grammar.grammar import Grammar
from models.parser.backtrack_frame import BacktrackFrame
from models.parser.match import Match
from models.parser.parse_result import ParseResult
from models.parser.parser_state import ParserState


class ParserEngine:

    def __init__(self, grammar: Grammar, forest_builder: ForestBuilder):
        self.__grammar = grammar
        self.__forest_builder = forest_builder
        self.__step_counter = 0
        self.__input_symbols: list[str] = []

    def parse(self, input_symbols: list[str]) -> ParseResult:
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
                OutputFormatter.record_step(
                    step_number=self.__step_counter,
                    action="REDUCE",
                    state=candidate_state,
                    production=match.production.format()
                )

                # We apply recursion
                result = self.__search(candidate_state)
                if result is not None:
                    return result

                # If the result is None, we have to backtrack
                restored_state = base_state.clone()
                self.__forest_builder.state = restored_state

                self.__step_counter += 1
                OutputFormatter.record_step(
                    step_number=self.__step_counter,
                    action="BACKTRACK",
                    state=restored_state,
                    undo=match.production.format(),
                )

                # if match_index < len(matches) - 1:
                #     frame.alternatives = matches[match_index + 1:]

            # If we have no matches left, we shift a symbol
            if state.remaining_input:
                shifted_state = base_state.clone()
                symbol = state.remaining_input[0]

                self.__forest_builder.state = shifted_state
                self.__forest_builder.apply_shift(symbol)

                self.__step_counter += 1
                OutputFormatter.record_step(
                    step_number=self.__step_counter,
                    action="SHIFT",
                    state=shifted_state,
                    symbol=symbol,
                )

                return self.__search(shifted_state)

        if state.remaining_input:
            shifted_state = state.clone()
            symbol = state.remaining_input[0]

            self.__forest_builder.state = shifted_state
            self.__forest_builder.apply_shift(symbol)

            self.__step_counter += 1
            OutputFormatter.record_step(
                step_number=self.__step_counter,
                action="SHIFT",
                state=shifted_state,
                symbol=symbol,
            )

            return self.__search(shifted_state)
        return None

    def __find_matches(self, state: ParserState) -> list[Match]:
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
        return self.__step_counter