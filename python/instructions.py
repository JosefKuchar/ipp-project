from instruction import BaseInstruction, DataType
from error import exit_program, StatusCode
from frame import Frame
from arguments import Arguments
import sys

class Move(BaseInstruction):
    """MOVE <var> <symb>"""
    def execute(self):
        var = self.runner.frames.get_variable(self.args[0].value)
        var.set(self.runner.frames.get_variable(self.args[1].value))

class CreateFrame(BaseInstruction):
    """CREATEFRAME"""
    def execute(self):
        self.runner.frames.temporary_frame = Frame()

class PushFrame(BaseInstruction):
    """PUSHFRAME"""
    def execute(self):
        self.runner.frames.local_frame.push_frame()

class PopFrame(BaseInstruction):
    """POPFRAME"""
    def execute(self):
        self.runner.frames.local_frame.pop_frame()

class DefVar(BaseInstruction):
    """DEFVAR <var>"""
    def execute(self):
        self.runner.frames.create_variable(self.args[0].value)

class Call(BaseInstruction):
    """CALL <label>"""
    def execute(self):
        self.runner.call_stack.push(self.runner.next_ip)
        # TODO: Jump to label

class Return(BaseInstruction):
    """RETURN"""
    def execute(self):
        self.runner.next_ip = self.runner.call_stack.pop()

class PushS(BaseInstruction):
    """PUSHS <symb>"""
    def execute(self):
        evaled = self._evaluate_args()
        self.runner.stack.push(evaled[0])

class PopS(BaseInstruction):
    """POPS <var>"""
    def execute(self):
        evaled = self._evaluate_args()
        evaled[0].set(self.runner.stack.pop())

class Add(BaseInstruction):
    """ADD <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.INT or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value + evaled[2].value
        evaled[0].type = DataType.INT

class Sub(BaseInstruction):
    """SUB <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.INT or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value - evaled[2].value
        evaled[0].type = DataType.INT

class Mul(BaseInstruction):
    """MUL <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.INT or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value * evaled[2].value
        evaled[0].type = DataType.INT

class IDiv(BaseInstruction):
    """IDIV <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.INT or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[2].value == 0:
            exit_program(StatusCode.INVALID_VALUE, "Division by zero")
        evaled[0].value = evaled[1].value // evaled[2].value
        evaled[0].type = DataType.INT

class Lt(BaseInstruction):
    """LT <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type or evaled[1].type == DataType.NIL or evaled[2].type == DataType.NIL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value > evaled[2].value
        evaled[0].type = DataType.BOOL

class Gt(BaseInstruction):
    """GT <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type or evaled[1].type == DataType.NIL or evaled[2].type == DataType.NIL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value < evaled[2].value
        evaled[0].type = DataType.BOOL

class Eq(BaseInstruction):
    """EQ <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value == evaled[2].value
        evaled[0].type = DataType.BOOL

class And(BaseInstruction):
    """AND <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.BOOL or evaled[2].type != DataType.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value and evaled[2].value
        evaled[0].type = DataType.BOOL

class Or(BaseInstruction):
    """OR <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.BOOL or evaled[2].type != DataType.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value or evaled[2].value
        evaled[0].type = DataType.BOOL

class Not(BaseInstruction):
    """NOT <var> <symb>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = not evaled[1].value
        evaled[0].type = DataType.BOOL

class Int2Char(BaseInstruction):
    """INT2CHAR <var> <symb>"""
    def execute(self):
        pass

class Stri2Int(BaseInstruction):
    """STRI2INT <var> <symb1> <symb2>"""
    def execute(self):
        pass

class Read(BaseInstruction):
    """READ <var> <type>"""
    def execute(self):
        evaled = self._evaluate_args()
        args = Arguments.get_instance()

        with args.input as sys.stdin:
            input_str = input()
            if evaled[1].value == "int":
                evaled[0].value = int(input_str)
                evaled[0].type = DataType.INT
            elif evaled[1].value == "bool":
                if input_str == "true":
                    evaled[0].value = True
                else:
                    evaled[0].value = False
                evaled[0].type = DataType.BOOL
            elif evaled[1].value == "string":
                evaled[0].value = input_str
                evaled[0].type = DataType.STRING

class Write(BaseInstruction):
    """WRITE <symb>"""
    def execute(self):
        evaled = self._evaluate_args()
        # TODO: nil, bool
        print(evaled[0].value, end="")

class Concat(BaseInstruction):
    """CONCAT <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.STRING or evaled[2].type != DataType.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value + evaled[2].value
        evaled[0].type = DataType.STRING

class StrLen(BaseInstruction):
    """STRLEN <var> <symb>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = len(evaled[1].value)
        evaled[0].type = DataType.INT

class GetChar(BaseInstruction):
    """GETCHAR <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.STRING or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[2].value < 0 or evaled[2].value >= len(evaled[1].value):
            exit_program(StatusCode.INVALID_STRING, "Invalid argument value")
        evaled[0].value = evaled[1].value[evaled[2].value]
        evaled[0].type = DataType.STRING

class SetChar(BaseInstruction):
    """SETCHAR <var> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[0].type != DataType.STRING or evaled[1].type != DataType.INT or evaled[2].type != DataType.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[1].value < 0 or evaled[1].value >= len(evaled[0].value) or len(evaled[2].value) == 0:
            exit_program(StatusCode.INVALID_STRING, "Invalid argument value")
        evaled[0].value = evaled[0].value[:evaled[1].value] + evaled[2].value[0] + evaled[0].value[evaled[1].value + 1:]
        evaled[0].type = DataType.STRING

class Type(BaseInstruction):
    """TYPE <var> <symb>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type == DataType.NIL:
            evaled[0].value = "nil"
        elif evaled[1].type == DataType.INT:
            evaled[0].value = "int"
        elif evaled[1].type == DataType.BOOL:
            evaled[0].value = "bool"
        elif evaled[1].type == DataType.STRING:
            evaled[0].value = "string"
        elif evaled[1].type == None:
            evaled[0].value = ""

class Label(BaseInstruction):
    """LABEL <label>"""
    def execute(self):
        pass # Labels are not executed

class Jump(BaseInstruction):
    """JUMP <label>"""
    def execute(self):
        evaled = self._evaluate_args()
        self.runner.jump_to_label(evaled[0].value)

class JumpIfEq(BaseInstruction):
    """JUMPIFEQ <label> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        # TODO: Type checking
        if evaled[1].value == evaled[2].value:
            self.runner.jump_to_label(evaled[0].value)

class JumpIfNeq(BaseInstruction):
    """JUMPIFNEQ <label> <symb1> <symb2>"""
    def execute(self):
        evaled = self._evaluate_args()
        # TODO: Type checking
        if evaled[1].value != evaled[2].value:
            self.runner.jump_to_label(evaled[0].value)

class Exit(BaseInstruction):
    """EXIT <symb>"""
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[0].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[0].value < 0 or evaled[0].value > 49:
            exit_program(StatusCode.INVALID_VALUE, "Invalid argument value")
        exit(evaled[0].value)

class DPrint(BaseInstruction):
    """DPRINT <symb>"""
    def execute(self):
        print("TODO DPRINT INFO", file=sys.stderr)

class Break(BaseInstruction):
    """BREAK"""
    def execute(self):
        print("TODO BREAK INFO", file=sys.stderr)
