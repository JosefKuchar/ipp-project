"""Functions for error handling"""

from enum import Enum
import sys


class StatusCode(Enum):
    """Possible status codes"""
    OK = 0
    MISSING_PARAM = 10
    INPUT_ERROR = 11
    OUTPUT_ERROR = 12
    MALLFORMED = 31
    INVALID_STRUCTURE = 32
    SEMANTIC_ERROR = 52
    INVALID_TYPE = 53
    MISSING_VAR = 54
    MISSING_FRAME = 55
    MISSING_VALUE = 56
    INVALID_VALUE = 57
    INVALID_STRING = 58
    INTERNAL_ERROR = 99


def exit_program(status_code, message):
    """Exit program with given status code and message"""
    print(message, file=sys.stderr)
    exit(status_code.value)
