from typing import Tuple, Type

from flake8_type_hinted import Argument
from flake8_type_hinted.checker import TypeHintChecker


class Error:
    """Represent linting error codes & relevant metadata."""

    def __init__(self, error_id: str, message: str):
        self.error_id = error_id
        self.message = message
        self.argname: str
        self.lineno: int
        self.col_offset: int

    def from_argument(self, argument: Argument):
        """Set error metadata from the input Argument object."""
        self.argname = argument.argname
        self.lineno = argument.lineno
        self.col_offset = argument.col_offset

    def to_flake8(self) -> Tuple[int, int, str, Type]:
        """
        Format the Error into what Flake8 is expecting.

        Expected output is a tuple with the following information:
          (line number, column number, message, type*)

        * I'm not sure what the type is currently used for, and could potentially be omitted
        """
        return (self.lineno, self.col_offset, self.message, TypeHintChecker)


# Function Annotations
class TYP001(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP001", "Missing type annotation for function argument '{}'")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset

    def to_flake8(self) -> Tuple[int, int, str, Type]:
        """Overload super's formatter so we can include argname in the output"""
        return (self.lineno, self.col_offset, self.message.format(self.argname), TypeHintChecker)


class TYP002(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP002", "Missing type annotation for *args")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP003(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP003", "Missing type annotation for **kwargs")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


# Method annotations
class TYP101(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP101", "Missing type annotation for self in class method")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP102(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP102", "Missing type annotation for cls in classmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


# Return annotations
class TYP201(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP201", "Missing return type annotation for public function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP202(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP202", "Missing return type annotation for protected function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP203(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP203", "Missing return type annotation for secret function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP204(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP204", "Missing return type annotation for magic function")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP205(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP205", "Missing return type annotation for staticmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset


class TYP206(Error):
    def __init__(self, argname: str, lineno: int, col_offset: int):
        super().__init__("TYP206", "Missing return type annotation for classmethod")
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset