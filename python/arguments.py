class Arguments(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Arguments, cls).__new__(cls)
        return cls.instance

    # # Parse args
    # def __init__(self):
    #     self.parser = "Test"
