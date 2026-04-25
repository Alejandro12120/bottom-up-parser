from dataclasses import dataclass

from models.node import Node
from models.parser.parser_state import ParserState


@dataclass(slots=True)
class ParseResult:
    accepted: bool
    final_state: ParserState
    final_root: Node | None