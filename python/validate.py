"""Validate XML structure"""

import re
from enum import Enum
from error import StatusCode, exit_program


class Arg(Enum):
    """Instruction argument type"""
    VARIABLE = 1
    SYMBOL = 2
    LABEL = 3
    TYPE = 4


# All instructions
INSTRUCTIONS = {
    'MOVE': [Arg.VARIABLE, Arg.SYMBOL],
    'CREATEFRAME': [],
    'PUSHFRAME': [],
    'POPFRAME': [],
    'DEFVAR': [Arg.VARIABLE],
    'CALL': [Arg.LABEL],
    'RETURN': [],
    'PUSHS': [Arg.SYMBOL],
    'POPS': [Arg.VARIABLE],
    'ADD': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'SUB': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'MUL': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'IDIV': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'LT': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'GT': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'EQ': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'AND': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'OR': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'NOT': [Arg.VARIABLE, Arg.SYMBOL],
    'INT2CHAR': [Arg.VARIABLE, Arg.SYMBOL],
    'STRI2INT': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'READ': [Arg.VARIABLE, Arg.TYPE],
    'WRITE': [Arg.SYMBOL],
    'CONCAT': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'STRLEN': [Arg.VARIABLE, Arg.SYMBOL],
    'GETCHAR': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'SETCHAR': [Arg.VARIABLE, Arg.SYMBOL, Arg.SYMBOL],
    'TYPE': [Arg.VARIABLE, Arg.SYMBOL],
    'LABEL': [Arg.LABEL],
    'JUMP': [Arg.LABEL],
    'JUMPIFEQ': [Arg.LABEL, Arg.SYMBOL, Arg.SYMBOL],
    'JUMPIFNEQ': [Arg.LABEL, Arg.SYMBOL, Arg.SYMBOL],
    'EXIT': [Arg.SYMBOL],
    'DPRINT': [Arg.SYMBOL],
    'BREAK': []
}

# Regex patterns
VAR_RE = re.compile(r"^([GLT]F@[_\-$\&%\*!\?a-zA-Z][_\-$\&%\*!\?a-zA-Z0-9]*)$")
LABEL_RE = re.compile(r"^([_\-$\&%\*!\?a-zA-Z][_\-$\&%\*!\?a-zA-Z0-9]*)$")
BOOL_RE = re.compile(r"^(true|false)$")
NIL_RE = re.compile(r"^nil$")
INT_RE = re.compile(
    r"^[+-]?((?:[1-9][0-9]*(_[0-9]+)*|0)|(?:0[xX][0-9a-fA-F]+(_[0-9a-fA-F]+)*)|(?:0[oO]?[0-7]+(_[0-7]+)*))$")
STRING_RE = re.compile(r"^(?:(?:\\\d{3})|[^\\])*$")
TYPE_RE = re.compile(r"^(int|string|bool)$")


def validate_xml(xml):
    try:
        """Validate XML structure"""
        root = xml.find('.')
        # Check if root has correct name
        if root.tag != "program":
            exit_program(StatusCode.INVALID_STRUCTURE, "Invalid root tag")
        # Check language
        if "language" not in root.attrib or root.attrib["language"] != "IPPcode23":
            exit_program(StatusCode.INVALID_STRUCTURE,
                         "Invalid root attribute language")
        # Check for invalid attributes
        valid_attributes = ["language", "name", "description"]
        for attribute in root.attrib:
            if attribute not in valid_attributes:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Invalid root attribute")

        labels = []
        orders = []

        # Check instructions
        for child in root:
            # Check if instruction has correct name
            if child.tag != "instruction":
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Invalid instruction tag")
            # Check number of attributes
            if len(child.attrib) != 2:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Invalid instruction attributes")
            # Check for invalid attributes
            valid_attributes = ["order", "opcode"]
            for attribute in child.attrib:
                if attribute not in valid_attributes:
                    exit_program(StatusCode.INVALID_STRUCTURE,
                                 "Invalid instruction attribute")
            # Check order
            order = child.attrib["order"]
            if not order.isnumeric() or int(order) < 1:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Invalid instruction order")
            if int(order) in orders:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Duplicate instruction order")
            orders.append(int(order))
            # Check for invalid opcode
            opcode = child.attrib["opcode"].upper()
            if opcode not in INSTRUCTIONS:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Invalid instruction opcode")
            # Check for invalid number of arguments
            if len(child) != len(INSTRUCTIONS[opcode]):
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Invalid number of arguments")
            # Check argument names
            arg_names = ["arg" + str(x + 1) for x in range(len(child))]
            for index, arg in enumerate(arg_names):
                argument = child.find(arg)
                if argument is None:
                    exit_program(StatusCode.INVALID_STRUCTURE,
                                 "Invalid argument name")
                if len(argument.attrib) != 1 or "type" not in argument.attrib:
                    exit_program(StatusCode.INVALID_STRUCTURE,
                                 "Invalid argument attributes")
                arg_type = INSTRUCTIONS[opcode][index]
                text = argument.text
                if text is not None:
                    text = text.strip()
                if arg_type == Arg.VARIABLE:
                    if argument.attrib["type"] != "var":
                        exit_program(StatusCode.INVALID_STRUCTURE,
                                     "Invalid argument type")
                    if not VAR_RE.match(text):
                        exit_program(StatusCode.INVALID_STRUCTURE,
                                     "Invalid variable name")
                elif arg_type == Arg.SYMBOL:
                    if argument.attrib["type"] not in ["var", "int", "string", "bool", "nil"]:
                        exit_program(StatusCode.INVALID_STRUCTURE,
                                     "Invalid argument type")
                    if argument.attrib["type"] == "var":
                        if not VAR_RE.match(text):
                            exit_program(StatusCode.INVALID_STRUCTURE,
                                         "Invalid variable name")
                    elif argument.attrib["type"] == "int":
                        if not INT_RE.match(text):
                            exit_program(StatusCode.INVALID_STRUCTURE,
                                         "Invalid integer")
                    elif argument.attrib["type"] == "string":
                        if text is not None and not STRING_RE.match(text):
                            exit_program(StatusCode.INVALID_STRUCTURE,
                                         "Invalid string")
                    elif argument.attrib["type"] == "bool":
                        if not BOOL_RE.match(text):
                            exit_program(StatusCode.INVALID_STRUCTURE,
                                         "Invalid boolean")
                    elif argument.attrib["type"] == "nil":
                        if not NIL_RE.match(text):
                            exit_program(StatusCode.INVALID_STRUCTURE,
                                         "Invalid nil")
                elif arg_type == Arg.LABEL:
                    if argument.attrib["type"] != "label":
                        exit_program(StatusCode.INVALID_STRUCTURE,
                                     "Invalid argument type")
                    if not LABEL_RE.match(text):
                        exit_program(StatusCode.INVALID_STRUCTURE,
                                     "Invalid label name")
                    if opcode == "LABEL":
                        if text in labels:
                            exit_program(StatusCode.SEMANTIC_ERROR,
                                         "Label already defined")
                        labels.append(text)
                elif arg_type == Arg.TYPE:
                    if argument.attrib["type"] != "type":
                        exit_program(StatusCode.INVALID_STRUCTURE,
                                     "Invalid argument type")
                    if not TYPE_RE.match(text):
                        exit_program(StatusCode.INVALID_STRUCTURE,
                                     "Invalid type")
    except Exception as e:
        exit_program(StatusCode.INVALID_STRUCTURE, e)
