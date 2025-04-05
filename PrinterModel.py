# very simple 3d printer model
# (many details not included, e.g. dual extruder)

from PrinterModelValue import PrinterModelValue


class PrinterModel:

    def __init__(self):
        # hint: All values are stored as strings

        self.unit = "mm"
        # temperatures & fan
        self.bed_temp = PrinterModelValue()
        self.extruder_temp = PrinterModelValue()
        self.fan = PrinterModelValue()
        # general movement
        self.feedrate = "?"
        self.positioning_mode = "absolute"
        # extruder
        self.extruder_move_mode = "absolute"
        self.extruder_physical = PrinterModelValue()
        self.extruder_physical.set("0")
        self.extruder_logical = PrinterModelValue()
        self.extruder_logical.set("0")
        # XYZ current position
        self.position_x = PrinterModelValue()
        self.position_y = PrinterModelValue()
        self.position_z = PrinterModelValue()
        # XYZ position where "something" was printed
        self.print_position_x = PrinterModelValue()
        self.print_position_y = PrinterModelValue()
        self.print_position_z = PrinterModelValue()

    def set_fan(self, value):
        self.fan.set(value)

    def set_bed_temperature(self, value):
        self.bed_temp.set(value)

    def set_extruder_temperature(self, value):
        self.extruder_temp.set(value)

    def set_extruder_move_mode(self, value):
        if value != "relative" and value != "absolute":
            raise Exception("setExtruderMoveMode: Unexpected value: " + value)

        self.extruder_move_mode = value

    # reset "logical" extruder position
    def set_extruder_position(self, value):
        self.extruder_logical.set(value)

    def set_positioning_mode(self, value):
        if value != "relative" and value != "absolute":
            raise Exception("setPositioningMode: Unexpected value: " + value)

        self.positioning_mode = value

    def set_feedrate(self, value):
        self.feedrate = value

    def home(self, x, y):
        z = ""

        # if no specific X or Y given, home all three axis
        if x == "" and y == "":
            x = "0"
            y = "0"
            z = "0"

        if x != "":
            self._homex(x)
        if y != "":
            self._home_y(y)
        if z != "":
            self._home_z()

    def _homex(self, value):
        if value != "0":
            raise Exception("homeX: Unexpected value: " + value)
        # TODO: Is the positioning mode important here?
        self.position_x.set(value)

    def _home_y(self, value):
        if value != "0":
            raise Exception("homeY: Unexpected value: " + value)
        # TODO: Is the positioning mode important here?
        self.position_y.set(value)

    def _home_z(self):
        # TODO: Is the positioning mode important here?
        self.position_z.set("0")

    def print_linear(self, x, y, z, e):
        # TODO: if distance calculation will be added, this must be improved
        # if x != "" and y != "":
        #    self._printX(x)
        #    self._printY(y)
        # else:
        if x != "":
            self._print_x(x)
        if y != "":
            self._print_y(y)
        if z != "":
            self._print_z(z)
        if e != "":
            self._print_e(e)

    def print_cw(self, x, y, i, j, e):
        # TODO: if distance calculation will be added, this must be improved
        # if x != "" and y != "":
        #    self._printX(x)
        #    self._printY(y)
        # else:
        if x != "":
            self._print_x(x)
        if y != "":
            self._print_y(y)
        if e != "":
            self._print_e(e)

    def print_ccw(self, x, y, i, j, e):
        # TODO: if distance calculation will be added, this must be improved
        # if x != "" and y != "":
        #    self._printX(x)
        #    self._printY(y)
        # else:
        if x != "":
            self._print_x(x)
        if y != "":
            self._print_y(y)
        if e != "":
            self._print_e(e)

    def _print_x(self, value):
        # G1 print commands will usually not include the z direction
        # call printZPhysical here to remember the Z min/max values correctly
        self._print_z_physical(self.position_z.get())

        if self.positioning_mode != "absolute":
            raise Exception("relative X positions not implemented")

        # remember the start point
        self.print_position_x.set(self.position_x.get())

        self.position_x.set(value)

        # remember the end point
        self.print_position_x.set(value)

    def _print_y(self, value):
        # G1 print commands will usually not include the z direction
        # call printZPhysical here to remember the Z min/max values correctly
        self._print_z_physical(self.position_z.get())

        if self.positioning_mode != "absolute":
            raise Exception("relative Y positions not implemented")

        # remember the start point
        self.print_position_y.set(self.position_y.get())

        self.position_y.set(value)

        # remember the end point
        self.print_position_y.set(value)

    def _print_z_physical(self, value):
        # remember the start point
        self.print_position_z.set(self.position_z.get())

        self.position_z.set(value)

        # remember the end point
        self.print_position_z.set(value)

    def _print_z(self, value):
        match self.positioning_mode:
            case "absolute":
                self._print_z_physical(value)
            case "relative":
                if self.position_z.get() == "?":
                    raise Exception("printZ: relative Z move without initial positioning")

                new_position_z = str(float(self.position_z.get()) + float(value))
                self._print_z_physical(str(new_position_z))
            case _:
                raise Exception("printZ: Positioning mode unexpected: " + self.positioning_mode)

    def _print_e(self, value):
        match self.extruder_move_mode:
            case "absolute":
                new_physical = float(self.extruder_physical.get()) + float(value) - float(self.extruder_logical.get())
                new_logical = float(value)
            case "relative":
                new_physical = float(self.extruder_physical.get()) + float(value)
                new_logical = float(self.extruder_logical.get()) + float(value)
            case _:
                raise Exception("extruder move mode not implemented: " + self.extruder_move_mode)

        self.extruder_physical.set(str(new_physical))
        self.extruder_logical.set(str(new_logical))

    def move(self, x, y, z):
        # TODO: if distance calculation will be added, this must be improved
        # if x != "" and y != "":
        #    self._moveX(x)
        #    self._moveY(y)
        # else:
        if x != "":
            self._move_x(x)
        if y != "":
            self._move_y(y)
        if z != "":
            self._move_z(z)

    def _move_x(self, value):
        match self.positioning_mode:
            case "absolute":
                self.position_x.set(value)
            case _:
                raise Exception("moveX: Positioning mode unexpected: " + self.positioning_mode)

    def _move_y(self, value):
        match self.positioning_mode:
            case "absolute":
                self.position_y.set(value)
            case _:
                raise Exception("moveY: Positioning mode unexpected: " + self.positioning_mode)

    def _move_z(self, value):
        match self.positioning_mode:
            case "absolute":
                self.position_z.set(value)
            case "relative":
                if self.position_z.get() == "?":
                    raise Exception("moveZ: relative Z move without initial positioning")

                new_position_z = float(self.position_z.get()) + float(value)
                self.position_z.set(str(new_position_z))
            case _:
                raise Exception("moveZ: Positioning mode unexpected: " + self.positioning_mode)
