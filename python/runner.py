"""Code runner"""
from frame import FrameManager
from instruction_factory import instruction_factory
from error import StatusCode, exit_program
from stack import Stack
from instructions import Label
from validate import validate_xml


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

    def check_label_exists(self, label):
        """Check if label exists"""
        for instruction in self.instructions:
            if isinstance(instruction, Label) and instruction.args[0].value == label:
                return
        exit_program(StatusCode.SEMANTIC_ERROR, "Label not found")

    def jump_to_label(self, label):
        """Jump to label"""
        for index, instruction in enumerate(self.instructions):
            if isinstance(instruction, Label) and instruction.args[0].value == label:
                self.next_ip = index
                return
        exit_program(StatusCode.SEMANTIC_ERROR, "Label not found")

    def _execute(self):
        # If instruction pointer is out of range, end the program
        if self.instruction_pointer >= len(self.instructions):
            self.done = True
        else:
            self.instructions[self.instruction_pointer].execute()

    def _parse_instructions(self, xml):
        validate_xml(xml)
        instructions = []
        # Parse and create instructions
        for instruction in xml.findall("instruction"):
            instructions.append(instruction_factory(instruction, self))
        # Sort instructions by order
        instructions = sorted(
            instructions, key=lambda instruction: instruction.order)
        return instructions
