class CustomError(Exception):
    def __init__(self, *args):
        self.message = args[0]
