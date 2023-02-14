from instruction import BaseInstruction, DataType
from error import exit_program, StatusCode
from frame import Frame
from arguments import Arguments
import sys

class Move(BaseInstruction):
    def execute(self):
        var = self.runner.frames.get_variable(self.args[0].value)
        var.set(self.runner.frames.get_variable(self.args[1].value))

class CreateFrame(BaseInstruction):
    def execute(self):
        self.runner.frames.temporary_frame = Frame()

class PushFrame(BaseInstruction):
    def execute(self):
        self.runner.frames.local_frame.push_frame()

class PopFrame(BaseInstruction):
    def execute(self):
        self.runner.frames.local_frame.pop_frame()

class DefVar(BaseInstruction):
    def execute(self):
        self.runner.frames.create_variable(self.args[0].value)

class Call(BaseInstruction):
    def execute(self):
        self.runner.call_stack.push(self.runner.next_ip)
        # TODO: Jump to label

class Return(BaseInstruction):
    def execute(self):
        self.runner.next_ip = self.runner.call_stack.pop()

class PushS(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        self.runner.stack.push(evaled[0])

class PopS(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        evaled[0].set(self.runner.stack.pop())

class Add(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.INT or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value + evaled[2].value
        evaled[0].type = DataType.INT

class Sub(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.INT or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value - evaled[2].value
        evaled[0].type = DataType.INT

class Mul(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.INT or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value * evaled[2].value
        evaled[0].type = DataType.INT

class IDiv(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.INT or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[2].value == 0:
            exit_program(StatusCode.INVALID_VALUE, "Division by zero")
        evaled[0].value = evaled[1].value // evaled[2].value
        evaled[0].type = DataType.INT

class Lt(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type or evaled[1].type == DataType.NIL or evaled[2].type == DataType.NIL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value > evaled[2].value
        evaled[0].type = DataType.BOOL

class Gt(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type or evaled[1].type == DataType.NIL or evaled[2].type == DataType.NIL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value < evaled[2].value
        evaled[0].type = DataType.BOOL

class Eq(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != evaled[2].type:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value == evaled[2].value
        evaled[0].type = DataType.BOOL

class And(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.BOOL or evaled[2].type != DataType.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value and evaled[2].value
        evaled[0].type = DataType.BOOL

class Or(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.BOOL or evaled[2].type != DataType.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value or evaled[2].value
        evaled[0].type = DataType.BOOL

class Not(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.BOOL:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = not evaled[1].value
        evaled[0].type = DataType.BOOL

class Int2Char(BaseInstruction):
    def execute(self):
        pass

class Stri2Int(BaseInstruction):
    def execute(self):
        pass

class Read(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        args = Arguments.get_instance()

        with args.input as sys.stdin:
            input_str = input() # TODO: Input from file
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
    def execute(self):
        evaled = self._evaluate_args()
        # TODO: nil, bool
        print(evaled[0].value, end="")

class Concat(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.STRING or evaled[2].type != DataType.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = evaled[1].value + evaled[2].value
        evaled[0].type = DataType.STRING

class StrLen(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        evaled[0].value = len(evaled[1].value)
        evaled[0].type = DataType.INT

class GetChar(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[1].type != DataType.STRING or evaled[2].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[2].value < 0 or evaled[2].value >= len(evaled[1].value):
            exit_program(StatusCode.INVALID_STRING, "Invalid argument value")
        evaled[0].value = evaled[1].value[evaled[2].value]
        evaled[0].type = DataType.STRING

class SetChar(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[0].type != DataType.STRING or evaled[1].type != DataType.INT or evaled[2].type != DataType.STRING:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[1].value < 0 or evaled[1].value >= len(evaled[0].value) or len(evaled[2].value) == 0:
            exit_program(StatusCode.INVALID_STRING, "Invalid argument value")
        evaled[0].value = evaled[0].value[:evaled[1].value] + evaled[2].value[0] + evaled[0].value[evaled[1].value + 1:]
        evaled[0].type = DataType.STRING

class Type(BaseInstruction):
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
    def execute(self):
        pass # Labels are not executed

class Jump(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        self.runner.jump_to_label(evaled[0].value)

class JumpIfEq(BaseInstruction):
    def execute(self):
        pass

class JumpIfNeq(BaseInstruction):
    def execute(self):
        pass

class Exit(BaseInstruction):
    def execute(self):
        evaled = self._evaluate_args()
        if evaled[0].type != DataType.INT:
            exit_program(StatusCode.INVALID_TYPE, "Invalid argument type")
        if evaled[0].value < 0 or evaled[0].value > 49:
            exit_program(StatusCode.INVALID_VALUE, "Invalid argument value")
        exit(evaled[0].value)

class DPrint(BaseInstruction):
    def execute(self):
        print("TODO DPRINT INFO", file=sys.stderr)

class Break(BaseInstruction):
    def execute(self):
        print("TODO BREAK INFO", file=sys.stderr)
