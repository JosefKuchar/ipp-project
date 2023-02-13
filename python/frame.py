
from error import StatusCode, exit_program
from variable import Variable


class FrameManager:
    """Variable frame manager"""

    def __init__(self):
        self.temporary_frame = None
        self.global_frame = Frame()
        self.local_frames = FrameStack(self)

    def get_variable(self, var):
        """Get variable"""
        (frame, name) = var.split("@")
        if frame == "GF":
            return self.global_frame.get_variable(name)
        elif frame == "LF":
            return self.local_frames.top_frame().get_variable(name)
        elif frame == "TF":
            if self.temporary_frame is None:
                exit_program(StatusCode.MISSING_FRAME, "No temporary frame")
            return self.temporary_frame.get_variable(name)

    def create_variable(self, var):
        """Create variable"""
        (frame, name) = var.split("@")
        if frame == "GF":
            self.global_frame.create_variable(name)
        elif frame == "LF":
            self.local_frames.top_frame().create_variable(name)
        elif frame == "TF":
            if self.temporary_frame is None:
                exit_program(StatusCode.MISSING_FRAME, "No temporary frame")
            self.temporary_frame.create_variable(name)


class FrameStack:
    """Variable frame stack"""

    def __init__(self, manager):
        self.frames = []
        self.manager = manager

    def push_frame(self):
        """Push frame"""
        if self.manager.temporary_frame is None:
            exit_program(StatusCode.MISSING_FRAME, "No temporary frame")
        self.frames.append(self.manager.temporary_frame)
        self.manager.temporary_frame = None

    def pop_frame(self):
        """Pop frame"""
        if len(self.frames) == 0:
            exit_program(StatusCode.MISSING_FRAME, "No frames in stack")
        else:
            self.manager.temporary_frame = self.frames.pop()

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
