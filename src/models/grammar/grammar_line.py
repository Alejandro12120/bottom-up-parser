from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GrammarLine:
    number: int
    text: str
