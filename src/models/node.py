from dataclasses import dataclass, field


@dataclass(slots=True)
class Node:
    symbol: str
    production_id: int | None
    children: list[Node] = field(default_factory=list)

    def clone(self) -> Node:
        """This method returns a copy of the node and its children.

        :returns: A copy of the node
        """
        return Node(
            symbol=self.symbol,
            production_id=self.production_id,
            children=[child.clone() for child in self.children],
        )

    def label(self) -> str:
        """This method returns the label used to print the node.

        :returns: The node label
        """
        if self.production_id is None:
            return self.symbol
        return f"{self.symbol}/{self.production_id}"
