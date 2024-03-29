"""Instruction foundation"""

from enum import Enum
import re
from variable import Variable
from error import exit_program, StatusCode


class DataType(Enum):
    """Variable types"""
    INT = 1
    STRING = 2
    BOOL = 3
    NIL = 4
    LABEL = 5
    TYPE = 6
    VAR = 7

    @staticmethod
    def from_string(string):
        """Convert string to type"""
        if string == "int":
            return DataType.INT
        elif string == "bool":
            return DataType.BOOL
        elif string == "string":
            return DataType.STRING
        elif string == "nil":
            return DataType.NIL
        elif string == "label":
            return DataType.LABEL
        elif string == "type":
            return DataType.TYPE
        elif string == "var":
            return DataType.VAR
        else:
            exit_program(StatusCode.MALLFORMED, "Invalid argument type")


class Argument:
    """Instruction argument"""

    def __init__(self, xml):
        self.type = DataType.from_string(xml.attrib['type'])
        self.value = xml.text
        if self.value is not None:
            self.value = self.value.strip()
        if self.type == DataType.INT:
            self.value = self.value.lower()
            # Remove underscores, o
            self.value = re.sub(r"[_o]", "", self.value)
            # Hex
            if re.match(r"^[+-]?0x", self.value):
                self.value = int(self.value, 16)
            # Octal
            elif re.match(r"^[+-]?0", self.value):
                self.value = int(self.value, 8)
            # Decimal
            else:
                self.value = int(self.value, 10)
        elif self.type == DataType.STRING:
            if self.value is None:
                self.value = ""
            else:
                self.value = re.sub(r"\\\d{3}",
                                    lambda x: chr(int(x.group(0)[1:])), self.value)
        elif self.type == DataType.BOOL:
            self.value = self.value == "true"


class BaseInstruction:
    """Base instruction"""

    def __init__(self, xml, runner):
        self.runner = runner
        self.order = int(xml.attrib['order'])
        self.args = []
        if xml.find('arg1') is not None:
            self.args.append(Argument(xml.find('arg1')))
        if xml.find('arg2') is not None:
            self.args.append(Argument(xml.find('arg2')))
        if xml.find('arg3') is not None:
            self.args.append(Argument(xml.find('arg3')))
        self.opcode = xml.attrib['opcode']

    def _evaluate_args(self, must_be_initialized=None):
        evaluated = []
        for index, arg in enumerate(self.args):
            var = None
            if arg.type == DataType.VAR:
                var = self.runner.frames.get_variable(arg.value)
            else:
                var = Variable(None, arg.type, arg.value)
            if must_be_initialized is not None and index in must_be_initialized:
                var.check_initialized()
            evaluated.append(var)
        return evaluated
