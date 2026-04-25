from dataclasses import dataclass

from components.error_handler import ErrorHandler
from models.grammar.production import Production


@dataclass(slots=True)
class Grammar:
    terminals: set[str]
    nonterminals: set[str]
    start_symbol: str
    productions: list[Production]
    by_left_side: dict[str, list[Production]]

    def validate_no_unit_cycles(self):
        """This method checks if the grammar contains any unit cycles

        :raises ParserError: if the grammar contains unit cycles
        """

        # The method we are going to use here is pretty simple, we are going to create a graph using
        # unit rules, for example: S -> A, A -> S
        # After that we are going to use DFS, that way for each symbol we are going to throw DFS and check
        # if we are able to arrive to a symbol that was previously visited in the current path.

        # We are going to use an adjacent array representation for the graph
        graph: dict[str, set[str]] = {symbol: set() for symbol in self.nonterminals}

        for production in self.productions:
            # Check if it is a unit production
            if len(production.right_side) == 1 and production.right_side[0] in self.nonterminals:
                graph[production.left_side].add(production.right_side[0])

        visiting: set[str] = set()  # This is the current path of each DFS
        visited: set[
            str] = set()  # Each node that was successfully checked there is no need to explore it again, so we insert it here.

        # This is going to be our recursive function to DFS
        def visit(symbol: str) -> bool:
            # if the node is already in the current recursion path,
            # we found a cycle.
            if symbol in visiting:
                return True

            # if the node was already processed before, no need to explore it again.
            if symbol in visited:
                return False

            # mark the node as part of the current DFS path.
            visiting.add(symbol)

            # recursively visit all neighbors reachable through unit productions.
            for neighbor in graph[symbol]:
                if visit(neighbor):
                    return True

            # Remove the node from the current DFS path and mark it as fully processed.
            visiting.remove(symbol)
            visited.add(symbol)
            return False

        for symbol in graph:
            if visit(symbol):
                ErrorHandler.raise_error("Cyclic grammar is not supported.")
