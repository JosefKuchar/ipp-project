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
        if self.type == DataType.INT:
            self.value = int(xml.text)
        elif self.type == DataType.STRING:
            self.value = re.sub(r"\\\d{3}",
                                lambda x: chr(int(x.group(0)[1:])), xml.text)
        elif self.type == DataType.BOOL:
            self.value = xml.text == "true"


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

    def _evaluate_args(self):
        evaluated = []
        for arg in self.args:
            if arg.type == DataType.VAR:
                evaluated.append(self.runner.frames.get_variable(arg.value))
            else:
                evaluated.append(Variable(None, arg.type, arg.value))
        return evaluated
