from components.forest_builder import ForestBuilder
from models.grammar import Grammar
from models.match import Match
from models.parse_result import ParseResult
from models.parser_state import ParserState


class ParserEngine:

    def __init__(self, grammar: Grammar, forest_builder: ForestBuilder):
        self.__grammar = grammar
        self.__forest_builder = forest_builder
        self.__step_counter = 0
        self.__input_symbols: list[str] = []

    def parse(self, input_symbols: list[str]) -> ParseResult:
        self.__step_counter = 0
        self.__input_symbols = list(input_symbols)

        initial_state = ParserState(
            input_pos=0,
            forest=[],
            consumed=[],
            remaining_input=list(input_symbols),
            right_most_derivation_hist=[]
        )
        initial_state.build_full_forest()

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
            #choose the first matching reduction
             #save the remaining alternatives in the backtracking stack
             #apply the reduction
             #record a REDUCE step
             #if the forest contains one tree rooted at the start symbol
             #and its frontier equals the input word without '$':
             #return ACCEPT
             #continue
            pass

        pass

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
