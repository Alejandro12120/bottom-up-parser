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
    ) -> None:
        step = StepRecord(
            step_number=step_number,
            action=action,
            symbol=symbol,
            production=production,
            undo=undo,
            working_part=state.working_part(),
            frontier=state.frontier(),
            forest_snapshot="", # TODO: Implement a render forest function
        )

        if step_number > 1:
            print("")
        print(OutputFormatter.format_step(step))
        print("")

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
            # TODO: Implemente a render tree function
            sections.append("REVERSED RIGHTMOST DERIVATION")
            sections.append(OutputFormatter.format_derivation(result.final_state.right_most_derivation_hist))
        return "\n\n".join(section for section in sections if section)

    @staticmethod
    def format_derivation(history: list[int]) -> str:
        return f"({','.join(str(item) for item in history)})"
