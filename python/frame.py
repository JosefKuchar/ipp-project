
from error import StatusCode, exit_program
from variable import Variable


class FrameManager:
    """Variable frame manager"""

    def __init__(self):
        self.temporary_frame = Frame()
        self.global_frame = Frame()
        self.local_frames = FrameStack()


class FrameStack:
    """Variable frame stack"""

    def __init__(self):
        self.frames = []

    def push_frame(self, frame):
        """Push frame"""
        self.frames.append(frame)

    def pop_frame(self):
        """Pop frame"""
        if len(self.frames) == 0:
            exit_program(StatusCode.MISSING_FRAME, "No frames in stack")
        else:
            return self.frames.pop()

    def top_frame(self):
        """Get top frame"""
        if len(self.frames) == 0:
            exit_program(StatusCode.MISSING_FRAME, "No frames in stack")
        else:
            return self.frames[-1]


class Frame:
    """Variable frame"""

    def __init__(self):
        self._variables = {}

    def clear(self):
        """Clear frame"""
        self._variables = {}

    def get_variable(self, name):
        """Get variable"""
        if name in self._variables:
            return self._variables[name]
        else:
            exit_program(StatusCode.MISSING_VAR, "Variable not found")

    def create_variable(self, name):
        """Create variable"""
        if name in self._variables:
            exit_program(StatusCode.SEMANTIC_ERROR, "Variable already exists")
        else:
            self._variables[name] = Variable(name)

    def modify_variable(self, name, value, var_type):
        """Modify variable"""
        if name in self._variables:
            self._variables[name].set_value(value, var_type)
        else:
            exit_program(StatusCode.MISSING_VAR, "Variable not found")
