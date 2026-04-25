from dataclasses import dataclass

from models.parser.match import Match
from models.parser.parser_state import ParserState


@dataclass(slots=True)
class BacktrackFrame:
    state: ParserState
    alternatives: list[Match]