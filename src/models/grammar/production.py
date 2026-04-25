from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Production:
    id: int
    left_side: str
    right_side: list[str]

    def format(self) -> str:
        return f"{self.id}) {self.left_side} -> {' '.join(self.right_side)}"