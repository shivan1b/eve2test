class YamlIndenter:
    """
    Cleanly indent by two spaces every new line with every new context.
    Likewise, unindent if one comes out of context.
    """

    def __init__(self, spaces=2, fpath=None):
        self.level = 0
        self.spaces = spaces
        self.fpath = fpath

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def _get_indented_data(self, data):
        if set('[~!@#$%^&*()+{}";\']+$').intersection(data):
            ldata = data.split(":")
            ldata[1] = '"{}"'.format(ldata[1].strip())
            data = ": ".join(ldata)
        return "{}{}".format(" " * self.spaces * self.level, data)

    def print(self, data):
        indented_data = self._get_indented_data(data)
        print(indented_data)

    def write(self, data):
        indented_data = self._get_indented_data(data)
        with open(self.fpath, "a") as fp:
            fp.write("{}{}".format(indented_data, "\n"))
