from models.node import Node
from models.parser.parse_result import ParseResult
from models.parser.parser_state import ParserState
from models.step_record import StepRecord


class OutputFormatter:

    @staticmethod
    def record_step(
            step_number: int,
            action: str,
            state: ParserState,
            symbol: str | None = None,
            production: str | None = None,
            undo: str | None = None,
    ) -> str:
        step = StepRecord(
            step_number=step_number,
            action=action,
            symbol=symbol,
            production=production,
            undo=undo,
            working_part=state.working_part(),
            frontier=state.frontier(),
            forest_snapshot=OutputFormatter.render_forest(state.forest),
        )

        return OutputFormatter.format_step(step)

    @staticmethod
    def format_step(step: StepRecord) -> str:
        lines = [
            f"STEP {step.step_number}",
            f"ACTION : {step.action}",
        ]

        if step.symbol is not None:
            lines.append(f"SYMBOL : {step.symbol}")

        if step.production is not None:
            lines.append(f"PRODUCTION: {step.production}")

        if step.undo is not None:
            lines.append(f"UNDO : {step.undo}")

        lines.extend(
            [
                f"WORKING PART : {step.working_part}",
                f"FRONTIER : {step.frontier}",
                "FOREST",
                step.forest_snapshot,
            ]
        )

        return "\n".join(lines)

    @staticmethod
    def format_result(result: ParseResult):
        sections: list[str] = ["ACCEPTED" if result.accepted else "REJECTED"]

        if result.accepted and result.final_root is not None:
            sections.append("FINAL PARSE TREE")
            sections.append(OutputFormatter.render_tree(result.final_root))
            sections.append("REVERSED RIGHTMOST DERIVATION")
            sections.append(OutputFormatter.format_derivation(result.final_state.right_most_derivation_hist))
        return "\n\n".join(section for section in sections if section)

    @staticmethod
    def format_derivation(history: list[int]) -> str:
        return f"({','.join(str(item) for item in history)})"

    @staticmethod
    def render_forest(forest: list[Node]):
        if not forest:
            return "(empty)"

        lines: list[str] = []

        for index, node in enumerate(forest):
            lines.append(OutputFormatter.render_tree(node, root_prefix=f"[{index}] ", child_prefix="    "))

        return "\n".join(lines)

    @staticmethod
    def render_tree(node: Node, root_prefix: str = "", child_prefix: str = ""):
        # Final tree:
        #   S/1
        #   ├── S/2
        #   │   └── a
        #   └── A/4
        #       └── b
        # In each iteration each forest tree is:
        #  [0] S/1
        #      ├── S/2
        #      │   └── a
        #      └── A/4
        #          └── b

        lines = [f"{root_prefix}{node.label()}"]

        for child_index, child in enumerate(node.children):
            is_last = child_index == len(node.children) - 1

            branch = "└── " if is_last else "├── "
            extension = "    " if is_last else "│   "

            # Now we need a recursive function to render each child of the child node
            lines.extend(OutputFormatter.render_child(child, child_prefix, branch, extension))

        return "\n".join(lines)


    @staticmethod
    def render_child(node: Node, prefix: str, branch: str, extension: str):
        lines = [f"{prefix}{branch}{node.label()}"]

        for child_index, child in enumerate(node.children):
            is_last = child_index == len(node.children) - 1

            child_branch = "└── " if is_last else "├── "
            child_extension = "    " if is_last else "│   "

            # Call it recursively
            lines.extend(
                OutputFormatter.render_child(
                    child,
                    prefix + extension,
                    child_branch,
                    child_extension,
                )
            )
        return lines

