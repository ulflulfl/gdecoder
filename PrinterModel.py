# very simple 3d printer model
# (many details not included, e.g. dual extruder)

from PrinterModelValue import PrinterModelValue


class PrinterModel:

    def __init__(self):
        # hint: All values are stored as strings

        self.unit = "mm"
        # temperatures & fan
        self.bedTemp = PrinterModelValue()
        self.extruderTemp = PrinterModelValue()
        self.fan = PrinterModelValue()
        # general movement
        self.feedrate = "?"
        self.positioningMode = "absolute"
        # extruder
        self.extruderMoveMode = "absolute"
        self.extruderPhysical = PrinterModelValue()
        self.extruderPhysical.set("0")
        self.extruderLogical = PrinterModelValue()
        self.extruderLogical.set("0")
        # XYZ current position
        self.positionX = PrinterModelValue()
        self.positionY = PrinterModelValue()
        self.positionZ = PrinterModelValue()
        # XYZ position where "something" was printed
        self.printPositionX = PrinterModelValue()
        self.printPositionY = PrinterModelValue()
        self.printPositionZ = PrinterModelValue()

    def setFan(self, value):
        self.fan.set(value)

    def setBedTemperature(self, value):
        self.bedTemp.set(value)

    def setExtruderTemperature(self, value):
        self.extruderTemp.set(value)

    def setExtruderMoveMode(self, value):
        if value != "relative" and value != "absolute":
            raise Exception("setExtruderMoveMode: Unexpected value: " + value)

        self.extruderMoveMode = value

    # reset "logical" extruder position
    def setExtruderPosition(self, value):
        self.extruderLogical.set(value)

    def setPositioningMode(self, value):
        if value != "relative" and value != "absolute":
            raise Exception("setPositioningMode: Unexpected value: " + value)

        self.positioningMode = value

    def setFeedrate(self, value):
        self.feedrate = value

    def home(self, x, y):
        z = ""

        # if no specific X or Y given, home all three axis
        if x == "" and y == "":
            x = "0"
            y = "0"
            z = "0"

        if x != "":
            self._homeX(x)
        if y != "":
            self._homeY(y)
        if z != "":
            self._homeZ()

    def _homeX(self, value):
        if value != "0":
            raise Exception("homeX: Unexpected value: " + value)
        # TODO: Is the positioning mode important here?
        self.positionX.set(value)

    def _homeY(self, value):
        if value != "0":
            raise Exception("homeY: Unexpected value: " + value)
        # TODO: Is the positioning mode important here?
        self.positionY.set(value)

    def _homeZ(self):
        # TODO: Is the positioning mode important here?
        self.positionZ.set("0")

    def printLinear(self, x, y, z, e):
        # TODO: if distance calculation will be added, this must be improved
        # if x != "" and y != "":
        #    self._printX(x)
        #    self._printY(y)
        # else:
        if x != "":
            self._printX(x)
        if y != "":
            self._printY(y)
        if z != "":
            self._printZ(z)
        if e != "":
            self._printE(e)

    def printCW(self, x, y, i, j, e):
        # TODO: if distance calculation will be added, this must be improved
        # if x != "" and y != "":
        #    self._printX(x)
        #    self._printY(y)
        # else:
        if x != "":
            self._printX(x)
        if y != "":
            self._printY(y)
        if e != "":
            self._printE(e)

    def printCCW(self, x, y, i, j, e):
        # TODO: if distance calculation will be added, this must be improved
        # if x != "" and y != "":
        #    self._printX(x)
        #    self._printY(y)
        # else:
        if x != "":
            self._printX(x)
        if y != "":
            self._printY(y)
        if e != "":
            self._printE(e)

    def _printX(self, value):
        # G1 print commands will usually not include the z direction
        # call printZPhysical here to remember the Z min/max values correctly
        self._printZPhysical(self.positionZ.get())

        if self.positioningMode != "absolute":
            raise Exception("relative X positions not implemented")

        # remember the start point
        self.printPositionX.set(self.positionX.get())

        self.positionX.set(value)

        # remember the end point
        self.printPositionX.set(value)

    def _printY(self, value):
        # G1 print commands will usually not include the z direction
        # call printZPhysical here to remember the Z min/max values correctly
        self._printZPhysical(self.positionZ.get())

        if self.positioningMode != "absolute":
            raise Exception("relative Y positions not implemented")

        # remember the start point
        self.printPositionY.set(self.positionY.get())

        self.positionY.set(value)

        # remember the end point
        self.printPositionY.set(value)

    def _printZPhysical(self, value):
        # remember the start point
        self.printPositionZ.set(self.positionZ.get())

        self.positionZ.set(value)

        # remember the end point
        self.printPositionZ.set(value)

    def _printZ(self, value):
        match self.positioningMode:
            case "absolute":
                self._printZPhysical(value)
            case "relative":
                if self.positionZ.get() == "?":
                    raise Exception("printZ: relative Z move without initial positioning")

                newPositionZ = str(float(self.positionZ.get()) + float(value))
                self._printZPhysical(str(newPositionZ))
            case _:
                raise Exception("printZ: Positioning mode unexpected: " + self.positioningMode)

    def _printE(self, value):
        match self.extruderMoveMode:
            case "absolute":
                newPhysical = float(self.extruderPhysical.get()) + float(value) - float(self.extruderLogical.get())
                newLogical = float(value)
            case "relative":
                newPhysical = float(self.extruderPhysical.get()) + float(value)
                newLogical = float(self.extruderLogical.get()) + float(value)
            case _:
                raise Exception("extruder move mode not implemented: " + self.extruderMoveMode)

        self.extruderPhysical.set(str(newPhysical))
        self.extruderLogical.set(str(newLogical))

    def move(self, x, y, z):
        # TODO: if distance calculation will be added, this must be improved
        # if x != "" and y != "":
        #    self._moveX(x)
        #    self._moveY(y)
        # else:
        if x != "":
            self._moveX(x)
        if y != "":
            self._moveY(y)
        if z != "":
            self._moveZ(z)

    def _moveX(self, value):
        match self.positioningMode:
            case "absolute":
                self.positionX.set(value)
            case _:
                raise Exception("moveX: Positioning mode unexpected: " + self.positioningMode)

    def _moveY(self, value):
        match self.positioningMode:
            case "absolute":
                self.positionY.set(value)
            case _:
                raise Exception("moveY: Positioning mode unexpected: " + self.positioningMode)

    def _moveZ(self, value):
        match self.positioningMode:
            case "absolute":
                self.positionZ.set(value)
            case "relative":
                if self.positionZ.get() == "?":
                    raise Exception("moveZ: relative Z move without initial positioning")

                newPositionZ = float(self.positionZ.get()) + float(value)
                self.positionZ.set(str(newPositionZ))
            case _:
                raise Exception("moveZ: Positioning mode unexpected: " + self.positioningMode)
