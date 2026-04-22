from dataclasses import dataclass

from models.node import Node


@dataclass(slots=True)
class ParserState:
    input_pos: int
    forest: list[Node]
    consumed: list[Node]
    remaining_input: list[str]
    right_most_derivation_hist: list[int]

    def clone(self) -> "ParserState":
        return ParserState(
            input_pos=self.input_pos,
            forest=[node.clone() for node in self.forest],
            consumed=[node.clone() for node in self.consumed],
            remaining_input=list(self.remaining_input),
            right_most_derivation_hist=list(self.right_most_derivation_hist),
        )

    def working_part(self) -> str:
        return "".join(node.symbol for node in self.consumed)

    def frontier(self) -> str:
        return "".join(self.remaining_input)
