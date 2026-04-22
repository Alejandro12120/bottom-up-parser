from dataclasses import dataclass

from models.production import Production


@dataclass(slots=True, frozen=True)
class Match:
    production: Production
    start_index: int
    end_index: int