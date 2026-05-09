from dataclasses import dataclass
from pathlib import Path
import difflib
import subprocess
import sys


@dataclass(slots=True)
class FunctionalTest:
    id: str
    words_path: str
    grammar_path: str
    expected_path: str



TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
MAIN_FILE = SRC_DIR / "main.py"

OUTPUT_FILE = TESTS_DIR / "output.txt"

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip()


def compare_outputs(expected: str, actual: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )
    )


def run_test(test: FunctionalTest) -> bool:
    grammar_file = TESTS_DIR / test.grammar_path
    words_file = TESTS_DIR / test.words_path
    expected_file = TESTS_DIR / test.expected_path

    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    result = subprocess.run(
        [
            sys.executable,
            str(MAIN_FILE),
            str(grammar_file),
            str(words_file),
            str(OUTPUT_FILE),
        ],
        capture_output=True,
        text=True,
    )

    if not OUTPUT_FILE.exists():
        print(f"{test.id} FAILED")
        print("  File output.txt was not created")

        if result.stdout:
            print("\nSTDOUT:")
            print(result.stdout)

        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)

        return False

    expected = read_file(expected_file)
    actual = read_file(OUTPUT_FILE)

    OUTPUT_FILE.unlink()

    if actual == expected:
        print(f"{test.id} PASSED")
        return True

    print(f"{test.id} FAILED")
    print()
    print(compare_outputs(expected, actual))

    if result.stdout:
        print("\nSTDOUT:")
        print(result.stdout)

    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)

    return False


def run_all_tests(tests_list: list[FunctionalTest]) -> None:
    passed = 0

    for test in tests_list:
        if run_test(test):
            passed += 1

        print()

    total = len(tests_list)
    print(f"Final result: {passed}/{total} tests passed.")

    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    tests: list[FunctionalTest] = [
        FunctionalTest(
            id="#1",
            words_path="words/a.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_1.txt",
        ),
        FunctionalTest(
            id="#2",
            words_path="words/ab.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_2.txt",
        ),
        FunctionalTest(
            id="#3",
            words_path="words/abb.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_3.txt",
        ),
        FunctionalTest(
            id="#4",
            words_path="words/abba.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_4.txt",
        ),
        FunctionalTest(
            id="#5",
            words_path="words/aa.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_5.txt",
        ),
        FunctionalTest(
            id="#6",
            words_path="words/b.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_6.txt",
        ),
        FunctionalTest(
            id="#7",
            words_path="words/empty_string.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_7.txt",
        ),
        FunctionalTest(
            id="#8",
            words_path="words/abba_missing_dollar.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_8.txt",
        ),
        FunctionalTest(
            id="#9",
            words_path="words/a.txt",
            grammar_path="grammars/missing_start.txt",
            expected_path="expected/result_9.txt",
        ),
        FunctionalTest(
            id="#10",
            words_path="words/a.txt",
            grammar_path="grammars/malformed_production.txt",
            expected_path="expected/result_10.txt",
        ),
        FunctionalTest(
            id="#11",
            words_path="words/a.txt",
            grammar_path="grammars/empty_right_side.txt",
            expected_path="expected/result_11.txt",
        ),
        FunctionalTest(
            id="#12",
            words_path="words/a.txt",
            grammar_path="grammars/cyclic_unit.txt",
            expected_path="expected/result_12.txt",
        ),
        FunctionalTest(
            id="#13",
            words_path="words/a.txt",
            grammar_path="grammars/epsilon_symbol.txt",
            expected_path="expected/result_13.txt",
        ),
        FunctionalTest(
            id="#14",
            words_path="words/a.txt",
            grammar_path="grammars/undefined_start.txt",
            expected_path="expected/result_14.txt",
        ),
        FunctionalTest(
            id="#15",
            words_path="words/a.txt",
            grammar_path="grammars/empty_alternative.txt",
            expected_path="expected/result_15.txt",
        ),
        FunctionalTest(
            id="#16",
            words_path="words/a.txt",
            grammar_path="grammars/invalid_left_side.txt",
            expected_path="expected/result_16.txt",
        ),
        FunctionalTest(
            id="#17",
            words_path="words/multiple_main_words.txt",
            grammar_path="grammars/main_recursive.txt",
            expected_path="expected/result_17.txt",
        ),
        FunctionalTest(
            id="#18",
            words_path="words/a.txt",
            grammar_path="grammars/simple_valid.txt",
            expected_path="expected/result_18.txt",
        ),
        FunctionalTest(
            id="#19",
            words_path="words/empty_word_between_words.txt",
            grammar_path="grammars/simple_valid.txt",
            expected_path="expected/result_19.txt",
        ),
    ]
    run_all_tests(tests)
