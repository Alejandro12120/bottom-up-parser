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
        """this method checks if the grammar contains any unit cycles.

        :raises ParserError: if the grammar contains unit cycles
        """

        # the method we are going to use here is pretty simple: we create a graph using
        # unit productions, for example: S -> A, A -> S.
        # after that, we run DFS from each nonterminal and check if we are able
        # to reach a symbol that is already in the current recursion path.

        # we are going to use an adjacency list representation for the graph.
        graph: dict[str, list[Production]] = {symbol: [] for symbol in self.nonterminals}

        for production in self.productions:
            # check if the production is a unit production.
            if len(production.right_side) == 1 and production.right_side[0] in self.nonterminals:
                graph[production.left_side].append(production)

        visiting: list[str] = []  # this is the current path of each DFS.
        visited: set[
            str] = set()  # each node that was successfully checked is inserted here, so we do not explore it again.

        # this is going to be our recursive DFS function.
        def visit(symbol: str, incoming_production: Production | None) -> tuple[list[str], Production | None] | None:
            """This function visits a symbol in the unit productions graph.

            :param symbol: The symbol to visit
            :param incoming_production: The production used to reach the symbol
            :returns: The detected cycle and production, or None if there is no cycle
            """
            # if the node is already in the current recursion path,
            # we found a cycle.
            if symbol in visiting:
                cycle_start = visiting.index(symbol)
                return visiting[cycle_start:] + [symbol], incoming_production

            # if the node was already processed before, there is no need to explore it again.
            if symbol in visited:
                return None

            # mark the node as part of the current DFS path.
            visiting.append(symbol)

            # recursively visit all neighbors reachable through unit productions.
            for production in graph[symbol]:
                next_symbol = production.right_side[0]
                cycle = visit(next_symbol, production)

                if cycle is not None:
                    return cycle

            # remove the node from the current DFS path and mark it as fully processed.
            visiting.pop()
            visited.add(symbol)
            return None

        # we preserve the production order when choosing DFS roots, so the detected
        # cycle is stable and easier to understand in the error message.
        # For example, if we use only the self.nonterminals set instead, since set does not guarantee order
        # we can get the same cycle printed in a different ways
        # S -> A -> B -> S
        # or
        # A -> B -> S -> A
        # or
        # B -> S -> A -> B
        root_symbols: list[str] = []
        for production in self.productions:
            if production.left_side not in root_symbols:
                root_symbols.append(production.left_side)

        for symbol in root_symbols:
            cycle = visit(symbol, None)
            if cycle is None:
                continue

            cycle_symbols, production = cycle
            cycle_text = " -> ".join(cycle_symbols)

            if production is not None and production.source_line is not None:
                # we print the line of the production which closed the cycle
                ErrorHandler.raise_error(
                    f"Grammar error at line {production.source_line}: "
                    f"expected grammar without unit cycles, found unit cycle {cycle_text}."
                )

            ErrorHandler.raise_error(
                f"Grammar error: expected grammar without unit cycles, found unit cycle {cycle_text}."
            )
