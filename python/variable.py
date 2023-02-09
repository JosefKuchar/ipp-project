from enum import Enum
from error import StatusCode, exit_program


class VariableType(Enum):
    """Variable types"""
    INT = 1
    STRING = 2
    BOOL = 3
    NIL = 4


class Variable:
    """Variable"""

    def __init__(self, name):
        self.name = name
        self.type = None
        self.value = None

    def set_value(self, value, var_type):
        """Set variable value"""
        self.value = value
        self.type = var_type

    def get_value(self):
        """Get variable value"""
        if self.value is None:
            exit_program(StatusCode.MISSING_VALUE, "Variable has no value")
        return self.value
