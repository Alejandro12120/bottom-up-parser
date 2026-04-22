from dataclasses import dataclass, field


@dataclass(slots=True)
class Node:
    symbol: str
    production_id: int | None
    children: list[Node] = field(default_factory=list)

    def clone(self) -> Node:
        return Node(
            symbol=self.symbol,
            production_id=self.production_id,
            children=[child.clone() for child in self.children],
        )

    def label(self) -> str:
        if self.production_id is None:
            return self.symbol
        return f"{self.symbol}/{self.production_id}"