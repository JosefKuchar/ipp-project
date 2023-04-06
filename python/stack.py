"""Stack implementation"""

from error import StatusCode, exit_program


class Stack:
    """Stack"""

    def __init__(self):
        self.items = []

    def push(self, item):
        """Push item to stack"""
        self.items.append(item)

    def pop(self):
        """Pop item from stack"""
        if len(self.items) == 0:
            exit_program(StatusCode.MISSING_VALUE, "Stack is empty")
        return self.items.pop()
