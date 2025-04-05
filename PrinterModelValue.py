# Keep a single float value with min and max.
# The value is kept as a string, with an initial "?" to distinguish this state from "real" values.
class PrinterModelValue:
    _value_current = "?"
    _value_max = "?"
    _value_min = "?"

    def set(self, value):
        self._value_current = value

        if self._value_max == "?":
            self._value_max = value

        if self._value_min == "?":
            self._value_min = value

        if float(value) > float(self._value_max):
            self._value_max = value

        if float(value) < float(self._value_min):
            self._value_min = value

    def get(self):
        return self._value_current

    def get_max(self):
        return self._value_max

    def get_min(self):
        return self._value_min
