from dataclasses import dataclass

from models.node import Node
from models.parser_state import ParserState
from models.step_record import StepRecord


@dataclass(slots=True)
class ParseResult:
    accepted: bool
    final_state: ParserState
    final_root: Node | None