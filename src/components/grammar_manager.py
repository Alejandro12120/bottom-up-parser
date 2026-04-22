from components.error_handler import ErrorHandler
from models.grammar import Grammar


class GrammarManager:

    def __init__(self, grammar_text: str):
        self.__grammar_text = grammar_text
        self.__grammar: Grammar | None = self.__parse_grammar()

    def __parse_grammar(self) -> Grammar | None:
        lines = [line.strip() for line in self.__grammar_text.splitlines() if line.strip()]
        if not lines:
            ErrorHandler.raise_error("Grammar file is empty.")

        start_symbol = GrammarManager.parse_start_declaration(lines[0])
        production_lines = lines[1:]
        if not production_lines:
            ErrorHandler.raise_error("Grammar file must contain at least one production.")

    @staticmethod
    def build_grammar(start_symbol, production_lines):
        nonterminals = GrammarManager.get_nonterminals(production_lines)
        if start_symbol not in nonterminals:
            ErrorHandler.raise_error("START symbol must appear on the left side of a production.")

    # PARSING GRAMMAR FUNCTIONS

    @staticmethod
    def parse_start_declaration(line: str):
        parts = line.split()
        if len(parts) != 2 or parts[0] != "START":
            ErrorHandler.raise_error("Missing START declaration.")

        return parts[1]

    @staticmethod
    def split_production(line: str) -> tuple[str, str, str]:
        """This method receives a production line and returns the left side, the arrow and the right side

        :param line: The production line
        :returns: A tuple (leftSide, arrow, rightSide)
        """
        if "->" not in line:
            ErrorHandler.raise_error(f"Malformed production line: {line}")

        left_raw, arrow, right_raw = line.partition("->")
        left_side = left_raw.strip()
        right_part = right_raw.strip()

        if arrow != "->" or not left_side or not right_part:
            ErrorHandler.raise_error(f"Malformed production line: {line}")

        if len(left_side.split()) != 1:
            ErrorHandler.raise_error(f"Malformed production line: {line}")

        return left_side, arrow, right_part

    @staticmethod
    def get_nonterminals(production_lines: list[str]) -> set[str]:
        """This method parses the production_lines to return a set of nonterminals

        :param production_lines: The production lines read from the grammar file.
        :returns: A set of nonterminals
        """

        nonterminals: set[str] = set()
        for line in production_lines:
            left_side, _, _ = GrammarManager.split_production(line)
            if len(left_side) > 1:
                ErrorHandler.raise_error("This is not a context-free grammar.")

            nonterminals.add(left_side)

        return nonterminals
