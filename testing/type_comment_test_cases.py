from textwrap import dedent
from typing import List, NamedTuple

from flake8_annotations import Argument
from flake8_annotations.enums import AnnotationType
from testing.helpers import typed_arg, untyped_arg


class ParserTestCase(NamedTuple):
    """Helper container for type comment test cases."""

    src: str
    args: List[Argument]
    should_yield_TYP301: bool


parser_test_cases = {
    "full_function_comment": ParserTestCase(
        src=dedent(
            """\
            def foo(arg1, arg2):
                # type: (int, int) -> int
                pass
            """
        ),
        args=[
            typed_arg(argname="arg1"),
            typed_arg(argname="arg2"),
            typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ],
        should_yield_TYP301=False,
    ),
    "partial_function_comment_no_ellipsis": ParserTestCase(
        src=dedent(
            """\
            def foo(arg1, arg2):
                # type: (int) -> int
                pass
            """
        ),
        args=[
            typed_arg(argname="arg1"),
            untyped_arg(argname="arg2"),
            typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ],
        should_yield_TYP301=False,
    ),
    "partial_function_comment_with_ellipsis": ParserTestCase(
        src=dedent(
            """\
            def foo(arg1, arg2):
                # type: (..., int) -> int
                pass
            """
        ),
        args=[
            untyped_arg(argname="arg1"),
            typed_arg(argname="arg2"),
            typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ],
        should_yield_TYP301=False,
    ),
    "argument_comments_ellipsis_function_comment": ParserTestCase(
        src=dedent(
            """\
            def foo(
                arg1,  # type: int
                arg2,  # type: int
            ):  # type: (...) -> int
                pass
            """
        ),
        args=[
            typed_arg(argname="arg1"),
            typed_arg(argname="arg2"),
            typed_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ],
        should_yield_TYP301=False,
    ),
    "argument_comments_no_function_comment": ParserTestCase(
        src=dedent(
            """\
            def foo(
                arg1,  # type: int
                arg2,  # type: int
            ):
                pass
            """
        ),
        args=[
            typed_arg(argname="arg1"),
            typed_arg(argname="arg2"),
            untyped_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ],
        should_yield_TYP301=False,
    ),
    "mixed_argument_hint_types": ParserTestCase(
        src=dedent(
            """\
            def foo(
                arg1,  # type: int
                arg2: int,
            ):
                pass
            """
        ),
        args=[
            typed_arg(argname="arg1"),
            typed_arg(argname="arg2", has_type_comment=False, has_3107_annotation=True),
            untyped_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ],
        should_yield_TYP301=True,
    ),
    "duplicate_argument_hint_types": ParserTestCase(
        src=dedent(
            """\
            def foo(
                arg1,  # type: int
                arg2: int,  # type: int
            ):
                pass
            """
        ),
        args=[
            typed_arg(argname="arg1"),
            typed_arg(argname="arg2", has_type_comment=True, has_3107_annotation=True),
            untyped_arg(argname="return", annotation_type=AnnotationType.RETURN),
        ],
        should_yield_TYP301=True,
    ),
    "arg_comment_return_annotation_hint_types": ParserTestCase(
        src=dedent(
            """\
            def foo(
                arg1,  # type: int
                arg2,  # type: int
            ) -> int:
                pass
            """
        ),
        args=[
            typed_arg(argname="arg1"),
            typed_arg(argname="arg2"),
            typed_arg(
                argname="return",
                annotation_type=AnnotationType.RETURN,
                has_type_comment=False,
                has_3107_annotation=True,
            ),
        ],
        should_yield_TYP301=True,
    ),
    "arg_annotation_return_comment_hint_types": ParserTestCase(
        src=dedent(
            """\
            def foo(
                arg1: int,
                arg2: int,
            ):  # type: (...) -> int
                pass
            """
        ),
        args=[
            typed_arg(argname="arg1", has_type_comment=False, has_3107_annotation=True),
            typed_arg(argname="arg2", has_type_comment=False, has_3107_annotation=True),
            typed_arg(
                argname="return", annotation_type=AnnotationType.RETURN, has_type_comment=True
            ),
        ],
        should_yield_TYP301=True,
    ),
}
