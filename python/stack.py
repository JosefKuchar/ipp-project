from error import StatusCode, exit_program

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) == 0:
            exit_program(StatusCode.MISSING_VALUE, "Stack is empty")
        return self.items.pop()
