from models.parser.match import Match
from models.node import Node
from models.parser.parser_state import ParserState
from models.grammar.production import Production


class ForestBuilder:
    """
    The ForestBuilder maintains the current partial parse forest throughout execution.
    """

    def __init__(self, state: ParserState):
        self.__state = state

    def apply_shift(self, symbol: str):
        """A shift operation does::
        - Create a terminal leaf node
        - Append it into the forest
        - Advance input position
        """

        # Keep in mind that the "forest" that the parser will use is the consumed
        # The forest attribute is used for printing
        # forest = consumed + remaining_input_as_terminal_nodes

        self.__state.consumed.append(ForestBuilder.make_terminal_node(symbol))

        if self.__state.remaining_input:
            self.__state.remaining_input.pop(0)
        self.__state.input_pos += 1

        self.__state.build_full_forest()

    def apply_reduction(self, match: Match):
        """This method applies reduction, that involves:
        - Get the nodes involved in the reduction
        - Create a reduction node using the production
        - Replace the nodes involved in the reduction by the reduction node
        """

        nodes_involved = self.__state.consumed[match.start_index: match.end_index]
        reduced = ForestBuilder.make_reduction_node(match.production, nodes_involved)

        self.__state.consumed = (
                self.__state.consumed[:match.start_index] + [reduced] + self.__state.consumed[match.end_index:]
        )

        self.__state.right_most_derivation_hist.append(match.production.id)
        self.__state.build_full_forest()

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, new_state: ParserState):
        self.__state = new_state

    @staticmethod
    def make_terminal_node(symbol: str) -> Node:
        """This function creates a node for a terminal (a leaf) from a symbol

        :param symbol: The nonterminal symbol
        :returns: The leaf node
        """
        return Node(symbol=symbol, production_id=None, children=[])

    @staticmethod
    def make_reduction_node(production: Production, children: list[Node]) -> Node:
        """Build and return a new reduction node.

        This function is used when a reduction applies.

        For example, if the forest looks like this::

            [0] S/2
                  └── a
            [1] A/4
                  └── b

        And the reduction rule is:
        S -> S A

        Then this function returns the following node::

            S/1
              ├── S/2
              │   └── a
              └── A/4
                  └── b

        :param production: The production rule used for the reduction.
        :param children: The nodes involved in the reduction.
        :return: A node whose symbol is the production's left-hand side symbol and whose
            children are the nodes involved in the reduction.
        """
        return Node(symbol=production.left_side, production_id=production.id,
                    children=[child.clone() for child in children])
