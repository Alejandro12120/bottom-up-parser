from collections import defaultdict

from components.error_handler import ErrorHandler
from models.grammar.grammar import Grammar
from models.grammar.grammar_line import GrammarLine
from models.grammar.production import Production


class GrammarManager:

    def __init__(self, grammar_text: str):
        self.__grammar_text = grammar_text
        self.__grammar: Grammar = self.__parse_grammar()

    def __parse_grammar(self) -> Grammar:
        lines = GrammarManager.collect_grammar_lines(self.__grammar_text)
        if not lines:
            ErrorHandler.raise_error("Grammar file is empty.")

        start_line = lines[0]

        start_symbol = GrammarManager.parse_start_declaration(start_line)

        production_lines = lines[1:]
        if not production_lines:
            ErrorHandler.raise_error(
                f"Grammar error after line {start_line.number}: "
                "expected at least one production after START declaration."
            )

        return GrammarManager.build_grammar(start_line, start_symbol, production_lines)

    @staticmethod
    def collect_grammar_lines(grammar_text: str) -> list[GrammarLine]:
        lines: list[GrammarLine] = []

        for number, raw_line in enumerate(grammar_text.splitlines(), start=1):
            stripped = raw_line.strip()
            if stripped:
                lines.append(GrammarLine(number=number, text=stripped))

        return lines

    @staticmethod
    def build_grammar(start_line: GrammarLine, start_symbol: str, production_lines: list[GrammarLine]):
        nonterminals = GrammarManager.get_nonterminals(production_lines)
        if start_symbol not in nonterminals:
            GrammarManager.raise_grammar_error(
                line=start_line,
                expected="START symbol to appear on the left side of a production",
                found=start_symbol,
            )

        productions = GrammarManager.parse_productions(production_lines)

        grammar = Grammar(
            terminals=GrammarManager.infer_terminals(nonterminals, productions),
            nonterminals=nonterminals,
            productions=productions,
            start_symbol=start_symbol,
            by_left_side=GrammarManager.group_by_left_side(productions)
        )

        # Because check if a grammar has every possible type of cycle is very hard
        # we are only going to check if the grammar has unit cycle
        # This type of cycle is very dangerous because we can loop infinitely between nonterminals
        # without generating any content

        grammar.validate_no_unit_cycles()

        return grammar

    @property
    def grammar(self) -> Grammar:
        return self.__grammar

    @staticmethod
    def raise_grammar_error(line: GrammarLine, expected: str, found: str | None = None) -> None:
        if found is None:
            found = line.text

        ErrorHandler.raise_error(
            f"Grammar error at line {line.number}: expected {expected}, found '{found}'"
        )

    # PARSING GRAMMAR FUNCTIONS

    @staticmethod
    def parse_start_declaration(line: GrammarLine):
        parts = line.text.split()
        if len(parts) != 2 or parts[0] != "START":
            GrammarManager.raise_grammar_error(
                line=line,
                expected="START declaration in format 'START <symbol>'",
            )

        return parts[1]

    @staticmethod
    def split_production(line: GrammarLine) -> tuple[str, str, str]:
        """This function receives a production line and returns the left side, the arrow and the right side

        :param line: The production line
        :returns: A tuple (leftSide, arrow, rightSide)
        """
        if "->" not in line.text:
            GrammarManager.raise_grammar_error(
                line=line,
                expected="production in format '<NonTerminal> -> <symbols>'",
            )

        left_raw, arrow, right_raw = line.text.partition("->")
        left_side = left_raw.strip()
        right_part = right_raw.strip()

        if arrow != "->":
            GrammarManager.raise_grammar_error(
                line=line,
                expected="production arrow '->'",
            )

        if not left_side:
            GrammarManager.raise_grammar_error(
                line=line,
                expected="one nonterminal before '->'",
            )

        if not right_part:
            GrammarManager.raise_grammar_error(
                line=line,
                expected="symbols after '->'",
            )

        left_symbols = left_side.split()
        if len(left_symbols) != 1:
            GrammarManager.raise_grammar_error(
                line=line,
                expected="exactly one nonterminal on the left side",
                found=left_side,
            )

        return left_side, arrow, right_part

    @staticmethod
    def get_nonterminals(production_lines: list[GrammarLine]) -> set[str]:
        """This function parses the production_lines to return a set of nonterminals

        :param production_lines: The production lines read from the grammar file.
        :returns: A set of nonterminals
        """

        nonterminals: set[str] = set()

        for line in production_lines:
            left_side, _, _ = GrammarManager.split_production(line)
            if len(left_side) > 1:
                GrammarManager.raise_grammar_error(
                    line=line,
                    expected="context-free production with one-symbol left side",
                    found=left_side,
                )

            nonterminals.add(left_side)

        return nonterminals

    @staticmethod
    def parse_productions(production_lines: list[GrammarLine]) -> list[Production]:
        """This function parses the production_lines and returns a list of Production objects.

        :param production_lines: The production lines read from the grammar file.
        :returns: A list of Production
        """

        productions: list[Production] = []
        production_id = 1

        for line in production_lines:
            left_side, _, right_side = GrammarManager.split_production(line)
            # S -> A s / B c
            alternatives = [alternative.strip() for alternative in right_side.split("/")]

            for alternative in alternatives:
                if not alternative:
                    GrammarManager.raise_grammar_error(
                        line=line,
                        expected="non-empty alternative after '/'",
                    )

                symbols = alternative.split()  # TODO: review, this, maybe is better the format S -> As / Bc
                if not symbols or 'ε' in symbols:
                    GrammarManager.raise_grammar_error(
                        line=line,
                        expected="non-empty symbols without epsilon",
                        found=alternative,
                    )

                productions.append(
                    Production(
                        id=production_id,
                        left_side=left_side,
                        right_side=symbols,
                        source_line=line.number,
                    )
                )
                production_id += 1

        return productions

    @staticmethod
    def infer_terminals(nonterminals: set[str], productions: list[Production]) -> set[str]:
        """This function uses the list of nonterminals and the list of Production to return a set of terminals symbols.

        :param nonterminals: A set of nonterminals
        :param productions: A list of Production
        :returns: A set of terminal symbols
        """
        terminals: set[str] = set()

        for production in productions:
            for symbol in production.right_side:
                if symbol not in nonterminals:
                    terminals.add(symbol)

        return terminals

    @staticmethod
    def group_by_left_side(productions: list[Production]) -> dict[str, list[Production]]:
        """This function uses the list of Production to return a dict where the keys are the nonterminal symbol
        and the values are a list of Production that uses that nonterminal.

        :param productions: A list of Production
        :returns: A dict where key: nonterminal, value: list[Production]
        """

        grouped: dict[str, list[Production]] = defaultdict(list)

        for production in productions:
            grouped[production.left_side].append(production)

        return grouped
