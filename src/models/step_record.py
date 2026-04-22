from dataclasses import dataclass


@dataclass(slots=True)
class StepRecord:
    step_number: int
    action: str
    symbol: str | None
    production: str | None
    undo: str | None
    working_part: str
    frontier: str
    forest_snapshot: str