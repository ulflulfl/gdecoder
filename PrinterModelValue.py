# Keep a single float value with min and max.
# The value is kept as a string, with an initial "?" to distinguish this state from "real" values.
class PrinterModelValue:
    _valueCurrent = "?"
    _valueMax = "?"
    _valueMin = "?"


    def set(self, value):
        self._valueCurrent = value

        if self._valueMax == "?":
            self._valueMax = value

        if self._valueMin == "?":
            self._valueMin = value

        if float(value) > float(self._valueMax):
            self._valueMax = value

        if float(value) < float(self._valueMin):
            self._valueMin = value

    def get(self):
        return self._valueCurrent

    def getMax(self):
        return self._valueMax

    def getMin(self):
        return self._valueMin
