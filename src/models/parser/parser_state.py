from dataclasses import dataclass

from models.grammar.grammar import Grammar
from models.node import Node


@dataclass(slots=True)
class ParserState:
    input_pos: int
    # Keep in mind that the "forest" that the parser will use is the consumed
    # The forest attribute is used for printing
    # forest = consumed + remaining_input_as_terminal_nodes
    forest: list[Node]
    consumed: list[Node]
    remaining_input: list[str]
    right_most_derivation_hist: list[int]

    def build_full_forest(self):
        """This method builds the total forest = consumed + remaining_input_as_terminal_nodes"""
        self.forest = list(self.consumed)

        self.forest.extend(
            Node(symbol=symbol, production_id=None, children=[])
            for symbol in self.remaining_input
        )
    def is_accepted(self, grammar: Grammar, input_symbols: list[str]) -> bool:
        """This method checks if the state is a valid state to accept the input string

        :param grammar: The grammar used by the parser
        :param input_symbols: The input symbols of the string that it should parse
        :returns: True if the word is accepted in this state, False if not
        """

        return (
            not self.remaining_input # There is no remaining input
            and len(self.consumed) == 1 # Our forest only have one tree
            and self.consumed[0].symbol == grammar.start_symbol # The symbol of the root matches the grammar's start symbol
            and ParserState.get_leaves(self.consumed[0]) == input_symbols
        )

    def clone(self) -> "ParserState":
        """This method returns a copy of the parser state.

        :returns: A copy of the parser state
        """
        return ParserState(
            input_pos=self.input_pos,
            forest=[node.clone() for node in self.forest],
            consumed=[node.clone() for node in self.consumed],
            remaining_input=list(self.remaining_input),
            right_most_derivation_hist=list(self.right_most_derivation_hist),
        )

    def working_part(self) -> str:
        """This method returns the consumed symbols as text.

        :returns: The working part
        """
        return "".join(node.symbol for node in self.consumed)

    def frontier(self) -> str:
        """This method returns the remaining input symbols as text.

        :returns: The frontier
        """
        return "".join(self.remaining_input)

    @staticmethod
    def get_leaves(node: Node) -> list[str]:
        """This function returns the leaves of a tree.

        :param node: The root node of the tree
        :returns: A list of leaf symbols
        """
        if not node.children:
            return [node.symbol]

        frontier: list[str] = []
        for child in node.children:
            frontier.extend(ParserState.get_leaves(child))

        return frontier
