from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Production:
    id: int
    left_side: str
    right_side: list[str]
    source_line: int | None = None

    def format(self) -> str:
        """This method formats the production as text.

        :returns: The formatted production
        """
        return f"{self.id}) {self.left_side} -> {' '.join(self.right_side)}"
