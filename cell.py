class Cell:
    def __init__(self, mined=False, value=0):
        # value: blank | mine | value(i)
        # state: showed | hidden

        self._showed = False
        self._marked = False

        self._mined = mined
        self._blank = value == 0 and not mined
        self._value = value

    def is_mined(self):
        return self._mined

    def is_blank(self):
        return self._blank

    def is_showed(self):
        return self._showed

    def is_marked(self):
        return self._marked

    def is_valued(self):
        return self._value > 0

    def number_of_mines(self):
        return self._value

    def show(self):
        self._showed = True

    def mark(self):
        self._marked = True

    def toggleMark(self):
        if not self._showed:
            self._marked = not self._marked

    def __str__(self):
        if self._marked and not self._showed:
            return "M"
        elif self._showed:
            if self._mined:
                return "X"
            elif self._blank:
                return "."
            else:
                return str(self._value)
        else:
            return " "
