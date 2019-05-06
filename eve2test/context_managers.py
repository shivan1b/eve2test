class YamlIndenter:
    """
    Cleanly indent by two spaces every new line with every new context.
    Likewise, unindent if one comes out of context.
    """
    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print(self, text):
        print("{}{}".format("  " * self.level, text))
