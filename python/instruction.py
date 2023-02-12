"""Instruction module"""
from enum import Enum
from error import StatusCode, exit_program


class Type(Enum):
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
            return Type.INT
        elif string == "bool":
            return Type.BOOL
        elif string == "string":
            return Type.STRING
        elif string == "nil":
            return Type.NIL
        elif string == "label":
            return Type.LABEL
        elif string == "type":
            return Type.TYPE
        elif string == "var":
            return Type.VAR
        else:
            exit_program(StatusCode.MALLFORMED, "Invalid argument type")


class Argument:
    """Instruction argument"""

    def __init__(self, xml):
        self.type = Type.from_string(xml.attrib['type'])
        self.value = xml.text


class Instruction:
    """Instruction"""

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


class InstructionFactory:
    """Instruction factory class"""


class AddInstruction:
    #runner.frames.
    """Add instruction"""
