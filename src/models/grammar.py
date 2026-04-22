from dataclasses import dataclass

from models.production import Production


@dataclass(slots=True)
class Grammar:
    terminals: set[str]
    nonterminals: set[str]
    start_symbol: str
    productions: list[Production]
    by_left_side: dict[str, list[Production]]

