"""Code runner"""
from frame import FrameManager
from instruction_factory import InstructionFactory
from instruction import DataType
from error import StatusCode, exit_program
from variable import Variable
from stack import Stack

class Runner:
    """Code runner"""

    def __init__(self, xml):
        self.instructions = []
        for instruction in xml.findall("instruction"):
            self.instructions.append(InstructionFactory(instruction, self))
        self._sort_and_check_instructions()
        self.done = False
        self.frames = FrameManager()
        self.stack = Stack()
        self.call_stack = Stack()
        self.instruction_pointer = 0
        self.next_ip = 0

    def run(self):
        """Run the code"""
        while not self.done:
            self.next_ip = self.instruction_pointer + 1
            self._execute()
            self.instruction_pointer = self.next_ip

    def jump_to_label(self, label):
        """Jump to label"""
        for instruction in self.instructions:
            if instruction.type == DataType.LABEL and instruction.args[0].value == label:
                self.next_ip = instruction.order
                return
        # TODO: Check error code
        exit_program(StatusCode.INVALID_STRUCTURE, "Label not found")

    def _execute(self):
        if self.instruction_pointer >= len(self.instructions):
            self.done = True
        else:
            self.instructions[self.instruction_pointer].execute()

    def _sort_and_check_instructions(self):
        self.instructions = sorted(
            self.instructions, key=lambda instruction: instruction.order)
        # Check for negative orders
        for instruction in self.instructions:
            if instruction.order < 0:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Negative instruction order")
        # Check for duplicate orders
        for i in range(len(self.instructions) - 1):
            if self.instructions[i].order == self.instructions[i + 1].order:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Duplicate instruction order")
