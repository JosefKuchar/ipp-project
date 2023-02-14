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
        self.instructions = self._parse_instructions(xml)
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
        exit_program(StatusCode.SEMANTIC_ERROR, "Label not found")

    def _execute(self):
        # If instruction pointer is out of range, end the program
        if self.instruction_pointer >= len(self.instructions):
            self.done = True
        else:
            self.instructions[self.instruction_pointer].execute()

    def _parse_instructions(self, xml):
        instructions = []
        # Parse and create instructions
        for instruction in xml.findall("instruction"):
            instructions.append(InstructionFactory(instruction, self))
        # Sort instructions by order
        instructions = sorted(instructions, key=lambda instruction: instruction.order)
        # Check for negative orders
        for instruction in instructions:
            if instruction.order < 0:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Negative instruction order")
        # Check for duplicate orders
        for i in range(len(instructions) - 1):
            if instructions[i].order == instructions[i + 1].order:
                exit_program(StatusCode.INVALID_STRUCTURE,
                             "Duplicate instruction order")
        # Check for duplicate labels
        labels = []
        for instruction in instructions:
            if instruction.type == DataType.LABEL:
                if instruction.args[0].value in labels:
                    exit_program(StatusCode.INVALID_STRUCTURE, "Duplicate label")
                labels.append(instruction.args[0].value)
        return instructions
