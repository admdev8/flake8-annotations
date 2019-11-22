import re
from typing import List, Tuple

import pytest
from flake8_annotations.checker import TypeHintChecker
from testing.helpers import parse_source

from .test_cases.variable_formatting_test_cases import variable_formatting_test_cases


ERROR_CODE_TYPE = Tuple[int, int, str, TypeHintChecker]
SIMPLE_ERROR_CODE = Tuple[str, str]

# Error type specific matching patterns
TEST_ARG_NAMES = {"TYP001": "some_arg", "TYP002": "some_args", "TYP003": "some_kwargs"}
RE_DICT = {"TYP001": r"'(\w+)'", "TYP002": r"\*(\w+)", "TYP003": r"\*\*(\w+)"}


def _simplify_error(error_code: ERROR_CODE_TYPE) -> SIMPLE_ERROR_CODE:
    """
    Simplify the error yielded by the flake8 checker into an (error type, argument name) tuple.

    Input error codes are assumed to be tuples of the form:
    (line number, column number, error string, checker class)

    Where the error string begins with "TYPxxx" and contains the arg name in the following form:
    TYP001: '{arg name}'
    TYP002: *{arg name}
    TYP003: **{arg name}
    """
    error_type = error_code[2].split()[0]
    arg_name = re.findall(RE_DICT[error_type], error_code[2])[0]
    return error_type, arg_name


class TestArgumentFormatting:
    """Testing class for containerizing parsed error codes & running the fixtured tests."""

    @pytest.fixture(params=variable_formatting_test_cases.items(),ids=variable_formatting_test_cases.keys())
    def parsed_errors(self, request) -> Tuple[List[SIMPLE_ERROR_CODE], str]:  # noqa: TYP001
        """
        Create a fixture for the error codes emitted by the test case source code.

        Error codes for the test case source code are simplified into a list of
        (error code, argument name) tuples.
        """
        test_case_name, test_case = request.param

        # Because TypeHintChecker is expecting a filename to initialize, rather than change this
        # logic use this file as a dummy, then update its tree & lines attributes in the fixture
        checker_instance = TypeHintChecker(None, __file__)
        tree, lines = parse_source(test_case.src)
        checker_instance.tree = tree
        checker_instance.lines = lines

        simplified_errors = [_simplify_error(error) for error in checker_instance.run()]

        return simplified_errors, test_case_name

    def test_arg_name(self, parsed_errors: Tuple[List[SIMPLE_ERROR_CODE], str]) -> None:
        """
        Check for correctly formatted argument names.

        Simplified error code information is provided by the fixture as a list of 
        (yielded error, test case name) tuples
        """
        assert all(
            TEST_ARG_NAMES[error_type] == arg_name for error_type, arg_name in parsed_errors[0]
        )
