from dataclasses import dataclass

from models.match import Match
from models.parser_state import ParserState


@dataclass(slots=True)
class BacktrackFrame:
    state: ParserState
    alternatives: list[Match]