"""Instruction module"""
from enum import Enum
from error import StatusCode, exit_program
from frame import Frame
from variable import Variable


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
        if self.type == Type.INT:
            self.value = int(xml.text)


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

    def _evaluate_args(self):
        evaluated = []
        for arg in self.args:
            if arg.type == Type.VAR:
                evaluated.append(self.runner.frames.get_variable(arg.value))
            else:
                evaluated.append(Variable(None, arg.type, arg.value))
        return evaluated

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
        self.runner.call_stack.push(self.runner.next_ip)
        # TODO: Jump to label

    def _return(self):
        self.runner.next_ip = self.runner.call_stack.pop()

    def _pushs(self):
        evaled = self._evaluate_args()
        self.runner.stack.push(evaled[0])

    def _pops(self):
        evaled = self._evaluate_args()
        evaled[0].set(self.runner.stack.pop())

    def _add(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.INT or evaled[2].type != Type.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value + evaled[2].value
        evaled[0].type = Type.INT

    def _sub(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.INT or evaled[2].type != Type.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value - evaled[2].value
        evaled[0].type = Type.INT

    def _mul(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.INT or evaled[2].type != Type.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value * evaled[2].value
        evaled[0].type = Type.INT

    def _idiv(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.INT or evaled[2].type != Type.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[2].value == 0:
            exit_program(StatusCode.INVALID_VALUE, "Division by zero")
        evaled[0].value = evaled[1].value // evaled[2].value
        evaled[0].type = Type.INT

    def _lt(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type or evaled[1].type == Type.NIL or evaled[2].type == Type.NIL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value < evaled[2].value
        evaled[0].type = Type.BOOL

    def _gt(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type or evaled[1].type == Type.NIL or evaled[2].type == Type.NIL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value > evaled[2].value
        evaled[0].type = Type.BOOL

    def _eq(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value == evaled[2].value
        evaled[0].type = Type.BOOL

    def _and(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.BOOL or evaled[2].type != Type.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value and evaled[2].value
        evaled[0].type = Type.BOOL

    def _or(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.BOOL or evaled[2].type != Type.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value or evaled[2].value
        evaled[0].type = Type.BOOL

    def _not(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = not evaled[1].value
        evaled[0].type = Type.BOOL

    def _int2char(self):
        pass

    def _stri2int(self):
        pass

    def _read(self):
        evaled = self._evaluate_args()
        input_str = input() # TODO: Input from file
        if evaled[1].value == "int":
            evaled[0].value = int(input_str)
            evaled[0].type = Type.INT
        elif evaled[1].value == "bool":
            if input_str == "true":
                evaled[0].value = True
            else:
                evaled[0].value = False
            evaled[0].type = Type.BOOL
        elif evaled[1].value == "string":
            evaled[0].value = input_str
            evaled[0].type = Type.STRING

    def _write(self):
        evaled = self._evaluate_args()
        # TODO: nil, bool
        print(evaled[0].value, end="")

    def _concat(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.STRING or evaled[2].type != Type.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value + evaled[2].value
        evaled[0].type = Type.STRING

    def _strlen(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = len(evaled[1].value)
        evaled[0].type = Type.INT

    def _getchar(self):
        evaled = self._evaluate_args()
        if evaled[1].type != Type.STRING or evaled[2].type != Type.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[2].value < 0 or evaled[2].value >= len(evaled[1].value):
            exit_program(StatusCode.INVALID_STRING, "Invalid argument value")
        evaled[0].value = evaled[1].value[evaled[2].value]
        evaled[0].type = Type.STRING

    def _setchar(self):
        evaled = self._evaluate_args()
        if evaled[0].type != Type.STRING or evaled[1].type != Type.INT or evaled[2].type != Type.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[1].value < 0 or evaled[1].value >= len(evaled[0].value) or len(evaled[2].value) == 0:
            exit_program(StatusCode.INVALID_STRING, "Invalid argument value")
        evaled[0].value = evaled[0].value[:evaled[1].value] + evaled[2].value[0] + evaled[0].value[evaled[1].value + 1:]
        evaled[0].type = Type.STRING

    def _type(self):
        evaled = self._evaluate_args()
        if evaled[1].type == Type.NIL:
            evaled[0].value = "nil"
        elif evaled[1].type == Type.INT:
            evaled[0].value = "int"
        elif evaled[1].type == Type.BOOL:
            evaled[0].value = "bool"
        elif evaled[1].type == Type.STRING:
            evaled[0].value = "string"
        elif evaled[1].type == None:
            evaled[0].value = ""

    def _label(self):
        pass

    def _jump(self):
        evaled = self._evaluate_args()
        self.runner.jump_to_label(evaled[0].value)

    def _jumpifeq(self):
        pass

    def _jumpifneq(self):
        pass

    def _exit(self):
        evaled = self._evaluate_args()
        if evaled[0].type != Type.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[0].value < 0 or evaled[0].value > 49:
            exit_program(StatusCode.INVALID_VALUE, "Invalid argument value")
        exit(evaled[0].value)

    def _dprint(self):
        pass

    def _break(self):
        pass
