"""Variable implementation"""

from error import StatusCode, exit_program


class Variable:
    """Variable"""

    def __init__(self, name, var_type=None, value=None):
        self.name = name
        self.type = var_type
        self.value = value

    def set(self, var):
        """Set variable value"""
        self.value = var.value
        self.type = var.type

    def check_initialized(self):
        """Check if variable is initialized"""
        if self.value is None and self.type is None:
            exit_program(StatusCode.MISSING_VALUE,
                         "Variable is not initialized")
