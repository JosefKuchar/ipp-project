"""Code runner"""
from frame import FrameManager
from instruction import Instruction
from error import StatusCode, exit_program


class Runner:
    """Code runner"""

    def __init__(self, xml):
        self.instructions = []
        for instruction in xml.findall("instruction"):
            self.instructions.append(Instruction(instruction))
        self._sort_and_check_instructions()
        print(self.instructions[0].__dict__)
        self.done = False
        self.frames = FrameManager()
        self.instruction_pointer = 0

    def run(self):
        """Run the code"""
        while not self.done:
            self._execute()
            self.instruction_pointer += 1

    def _execute(self):
        pass

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
