"""Instruction module"""
from enum import Enum
from error import StatusCode, exit_program
from frame import Frame


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
        self._opcodes = {
            "MOVE": self._move,
            "CREATEFRAME": self._createframe,
            "PUSHFRAME": self._pushframe,
            "POPFRAME": self._popframe,
            "DEFVAR": self._defvar,
            "CALL": self._call,
            "RETURN": self._return,
            "PUSHS": self._pushs,
            "POPS": self._pops,
            "ADD": self._add,
            "SUB": self._sub,
            "MUL": self._mul,
            "IDIV": self._idiv,
            "LT": self._lt,
            "GT": self._gt,
            "EQ": self._eq,
            "AND": self._and,
            "OR": self._or,
            "NOT": self._not,
            "INT2CHAR": self._int2char,
            "STRI2INT": self._stri2int,
            "READ": self._read,
            "WRITE": self._write,
            "CONCAT": self._concat,
            "STRLEN": self._strlen,
            "GETCHAR": self._getchar,
            "SETCHAR": self._setchar,
            "TYPE": self._type,
            "LABEL": self._label,
            "JUMP": self._jump,
            "JUMPIFEQ": self._jumpifeq,
            "JUMPIFNEQ": self._jumpifneq,
            "EXIT": self._exit,
            "DPRINT": self._dprint,
            "BREAK": self._break
        }

    def execute(self):
        """Execute the instruction"""
        if self.opcode in self._opcodes:
            self._opcodes[self.opcode]()
        else:
            exit_program(StatusCode.MALLFORMED, "Invalid opcode")

    def _move(self):
        var = self.runner.frames.get_variable(self.args[0].value)
        var.set(self.runner.frames.get_variable(self.args[1].value))

    def _createframe(self):
        self.runner.frames.temporary_frame = Frame()

    def _pushframe(self):
        self.runner.frames.local_frame.push_frame()

    def _popframe(self):
        self.runner.frames.local_frame.pop_frame()

    def _defvar(self):
        self.runner.frames.create_variable(self.args[0].value)

    def _call(self):
        pass

    def _return(self):
        pass

    def _pushs(self):
        pass

    def _pops(self):
        pass

    def _add(self):
        var = self.runner.frames.get_variable(self.args[0].value)
        var1 = self.runner.frames.get_variable(self.args[1].value)
        var2 = self.runner.frames.get_variable(self.args[2].value)

    def _sub(self):
        pass

    def _mul(self):
        pass

    def _idiv(self):
        pass

    def _lt(self):
        pass

    def _gt(self):
        pass

    def _eq(self):
        pass

    def _and(self):
        pass

    def _or(self):
        pass

    def _not(self):
        pass

    def _int2char(self):
        pass

    def _stri2int(self):
        pass

    def _read(self):
        pass

    def _write(self):
        var = self.runner.frames.get_variable(self.args[0].value)
        print(var.value)

    def _concat(self):
        pass

    def _strlen(self):
        pass

    def _getchar(self):
        pass

    def _setchar(self):
        pass

    def _type(self):
        pass

    def _label(self):
        pass

    def _jump(self):
        pass

    def _jumpifeq(self):
        pass

    def _jumpifneq(self):
        pass

    def _exit(self):
        pass

    def _dprint(self):
        pass

    def _break(self):
        pass
