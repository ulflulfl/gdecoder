# Decode a single line of gcode
#
# Limitation:
# The code expects a single command in each line.
# It will not work with multiple gcode commands in a single line.
#
# Hint: Many gcode details can be found at:
# https://reprap.org/wiki/G-code
# https://marlinfw.org/meta/gcode/


class GDecoderLine:

    stopOnUndecoded = False

    def error_undecodedGCode(self, line):
        message = "Unknown gcode: " + str(line)
        if self.stopOnUndecoded:
            raise Exception(message)
        else:
            return message

    def error_undecodedGCodeSubtoken(self, splitted, token):
        message = "Unknown subtoken: " + token + " in: " + str(splitted)
        if self.stopOnUndecoded:
            raise Exception(message)
        else:
            return ", " + message

    def error_firmwareDependentButUnknownGenerator(self, metaInfos, splitted):
        message = "Uexpected generator " + metaInfos.generator + " for firmware dependent: " + str(splitted)
        if self.stopOnUndecoded:
            raise Exception(message)
        else:
            return message

    def error_valueOutOfRange(self, line, value):
        message = "Value " + value + " out of range in: " + line
        if self.stopOnUndecoded:
            raise Exception(message)
        else:
            return ", " + message

    def decodeGCodeLine(self, metaInfos, line, printer):
        decoded = ""

        if line == "":
            return ""

        # avoid a strange gcode line (bug in Slic3r 1.37.2.1-prusa3d-win64?)
        if line == "Filament-specific end gcode":
            return ""

        # ignore comments and split into tokens
        uncommentedPart = line.split(";")[0]
        splitted = uncommentedPart.split()

        match splitted[0]:
            # G0: Rapid Move
            # https://marlinfw.org/docs/gcode/G000-G001.html
            case "G0":
                x = ""
                y = ""
                z = ""
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "F":
                            decoded += ", Feedrate: " + value + " " + printer.unit + "/min"
                            printer.setFeedrate(value)
                        case "G":
                            decoded = "Rapid Move (no print)"
                        case "X":
                            decoded += ", X: " + value + " " + printer.unit
                            x = value
                        case "Y":
                            decoded += ", Y: " + value + " " + printer.unit
                            y = value
                        case "Z":
                            decoded += ", Z: " + value + " " + printer.unit
                            z = value
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                # call move() after the (optional) feedrate was set
                printer.move(x, y, z)

                return decoded
            # G1: Linear Move
            # https://marlinfw.org/docs/gcode/G000-G001.html
            case "G1":
                x = ""
                y = ""
                z = ""
                e = ""
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "E":
                            decoded += ", E: " + value + " " + printer.unit
                            e = value
                        case "F":
                            decoded += ", Feedrate: " + value + " " + printer.unit + "/min"
                            printer.setFeedrate(value)
                        case "G":
                            decoded = "Linear Move (print)"
                        case "X":
                            decoded += ", X: " + value + " " + printer.unit
                            x = value
                        case "Y":
                            decoded += ", Y: " + value + " " + printer.unit
                            y = value
                        case "Z":
                            decoded += ", Z: " + value + " " + printer.unit
                            z = value
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                # call printLinear() after the feedrate was set
                printer.printLinear(x, y, z, e)

                return decoded
            # G2: Controlled Clockwise Arc Move
            case "G2":
                x = ""
                y = ""
                i = ""
                j = ""
                e = ""
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "E":
                            decoded += ", E: " + value + " " + printer.unit
                            e = value
                        case "F":
                            decoded += ", Feedrate: " + value + " " + printer.unit + "/min"
                            printer.setFeedrate(value)
                        case "G":
                            decoded = "Clockwise Arc Move (print)"
                        case "I":
                            decoded += ", I (distant X): " + value
                            i = value
                        case "J":
                            decoded += ", J (distant Y): " + value
                            j = value
                        case "X":
                            decoded += ", X:" + value
                            x = value
                        case "Y":
                            decoded += ", Y:" + value
                            y = value
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                printer.printCW(x, y, i, j, e)

                return decoded
            # G3: Controlled Counter-Clockwise Arc Move
            case "G3":
                x = ""
                y = ""
                i = ""
                j = ""
                e = ""
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "E":
                            decoded += ", E: " + value + " " + printer.unit
                            e = value
                        case "F":
                            decoded += ", Feedrate: " + value + " " + printer.unit + "/min"
                            printer.setFeedrate(value)
                        case "G":
                            decoded = "Counter-Clockwise Arc Move (print)"
                        case "I":
                            decoded += ", I (distant X): " + value
                            i = value
                        case "J":
                            decoded += ", J (distant Y): " + value
                            j = value
                        case "X":
                            decoded += ", X:" + value
                            x = value
                        case "Y":
                            decoded += ", Y:" + value
                            y = value
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                printer.printCCW(x, y, i, j, e)

                return decoded
            # G4: Dwell (aka Pause)
            case "G4":
                for token in splitted:
                    key = token[0]
                    match key:
                        case "G":
                            decoded = "Dwell (aka: Pause)"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # G21: Set Units to Millimeters
            case "G21":
                for token in splitted:
                    key = token[0]
                    match key:
                        case "G":
                            decoded = "Set Units to Millimeters"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # G28: Move to Origin (Home)
            # https://all3dp.com/2/g28-g-code-homing/
            # https://marlinfw.org/docs/gcode/G028.html
            # https://cncphilosophy.com/g28-g-code-demystified/
            case "G28":
                newX = ""
                newY = ""
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "F":
                            decoded += ", unknown parameter (maybe feedrate?): " + token
                            # TODO: What is this doing exactly?
                        case "G":
                            decoded = "Move to Origin (Home, often: X=0, Y=0; Z=0)"
                        case "W":
                            decoded += ", Suppress mesh bed leveling (Prusa only)"
                        case "X":
                            decoded += ", X axis origin: " + value
                            newX = value
                        case "Y":
                            decoded += ", Y axis origin: " + value
                            newY = value
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)

                printer.home(newX, newY)

                return decoded
            # G80: Mesh-based Z probe
            # https://marlinfw.org/docs/gcode/G080.html G80 - Cancel Current Motion Mode
            case "G80":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "G":
                            # TODO: What is this doing exactly?
                            decoded = "Mesh-based Z probe"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # G90: Set to Absolute Positioning
            # https://all3dp.com/2/g91-g90-g-code/
            # https://marlinfw.org/docs/gcode/G090.html
            case "G90":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "G":
                            decoded = "Set to Absolute Positioning"
                            printer.setPositioningMode("absolute")
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # G91: Set to Relative Positioning
            # https://all3dp.com/2/g91-g90-g-code/
            # https://marlinfw.org/docs/gcode/G091.html
            case "G91":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "G":
                            decoded = "Set to Relative Positioning"
                            printer.setPositioningMode("relative")
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # G92: Set Position
            case "G92":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "E":
                            decoded += ", new extruder position: " + value + " " + printer.unit
                            printer.setExtruderPosition(value)
                        case "G":
                            decoded = "Set Position"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M73: Set/Get build percentage
            case "M73":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Set/Get build percentage"
                        case "P":
                            decoded += ", Normal mode: " + value + " %"
                        case "Q":
                            decoded += ", Silent mode: " + value + " %"
                        case "R":
                            decoded += ", Remaining in normal mode: " + value + " min."
                        case "S":
                            decoded += ", Remaining in silent mode: " + value + " min."
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M82: Set extruder to absolute mode
            case "M82":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Set extruder to absolute mode"
                            printer.setExtruderMoveMode("absolute")
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M83: Set extruder to relative mode
            case "M83":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Set extruder to relative mode"
                            printer.setExtruderMoveMode("relative")
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M84: Stop idle hold
            case "M84":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Stop idle hold (disable motors)"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M104: Set Extruder Temperature
            case "M104":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Set Extruder Temperature"
                        case "S":
                            decoded += ", Target: " + value + " °C"
                            printer.setExtruderTemperature(value)
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M105: Get Extruder Temperature
            case "M105":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Get Extruder Temperature"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M106: Fan On
            case "M106":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Fan On"
                        case "S":
                            decoded += ", Fan Speed: " + value + " (0-255)"
                            printer.setFan(value)
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M107: Fan Off
            case "M107":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Fan Off"
                            printer.setFan("0")
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M109: Set Extruder Temperature and Wait
            case "M109":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Set Extruder Temperature and Wait"
                        case "S":
                            decoded += ", Target: " + value + " °C"
                            printer.setExtruderTemperature(value)
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M115: Get Firmware Version and Capabilities
            case "M115":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Get Firmware Version and Capabilities"
                        case "U":
                            decoded += ", Check the firmware version: " + value
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M117: Display Message
            case "M117":
                decoded = "Display Message: \"" + line[5:] + "\""
                return decoded
            # M140: Set Bed Temperature (Fast)
            case "M140":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Set Bed Temperature (Fast)"
                        case "S":
                            decoded += ", Target: " + value + " °C"
                            printer.setBedTemperature(value)
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M190: Wait for bed temperature to reach target temp
            case "M190":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded += "Wait for bed temperature to reach target temp"
                        case "S":
                            decoded += ", Target: " + value + " °C"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M201: Set max acceleration
            case "M201":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "E":
                            decoded += ", E: " + value + " " + printer.unit + "/s²"
                        case "M":
                            decoded = "Set max acceleration"
                        case "X":
                            decoded += ", X: " + value + " " + printer.unit + "/s²"
                        case "Y":
                            decoded += ", Y: " + value + " " + printer.unit + "/s²"
                        case "Z":
                            decoded += ", Z: " + value + " " + printer.unit + "/s²"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M203: Firmware dependent
            case "M203":
                decoded = ""
                if metaInfos.generator != "PrusaSlicer":
                    decoded = self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                # M203: Set maximum feedrate
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "E":
                            decoded += ", E: " + value + " " + printer.unit + "/s²"
                        case "M":
                            decoded += "Set maximum feedrate"
                        case "X":
                            decoded += ", X: " + value + " " + printer.unit + "/s²"
                        case "Y":
                            decoded += ", Y: " + value + " " + printer.unit + "/s²"
                        case "Z":
                            decoded += ", Z: " + value + " " + printer.unit + "/s²"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M204: Firmware dependent
            # https://reprap.org/wiki/G-code#M204:_Firmware_dependent
            case "M204":
                decoded = ""
                if metaInfos.generator != "PrusaSlicer" and metaInfos.generator != "Cura" and metaInfos.generator != "Slic3r":
                    decoded = self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                if metaInfos.generator == "Cura" and metaInfos.generator_flavor != "Marlin":
                    decoded += self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                # M204: Set default acceleration
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded += "Set default acceleration"
                        case "P":
                            decoded += ", printing: " + value + " " + printer.unit + "/s²"
                        case "R":
                            decoded += ", retract: " + value + " " + printer.unit + "/s²"
                        case "S":
                            decoded += ", normal: " + value + " " + printer.unit + "/s²"
                        case "T":
                            decoded += ", travel: " + value + " " + printer.unit + "/s²"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M205: Firmware dependent
            # https://reprap.org/wiki/G-code#M205:_Firmware_dependent
            case "M205":
                decoded = ""
                if metaInfos.generator != "PrusaSlicer" and metaInfos.generator != "Cura":
                    decoded = self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                if metaInfos.generator == "Cura" and metaInfos.generator_flavor != "Marlin":
                    decoded += self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                # M205: Advanced Settings
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "E":
                            decoded += ", E jerk: " + value + " " + printer.unit + "/s"
                        case "M":
                            decoded += "Advanced settings"
                        case "S":
                            decoded += ", min. print speed: " + value + " " + printer.unit + "/s"
                        case "T":
                            decoded += ", min. travel speed: " + value + " " + printer.unit + "/s"
                        case "X":
                            decoded += ", X Jerk: " + value + " " + printer.unit + "/s"
                        case "Y":
                            decoded += ", Y Jerk: " + value + " " + printer.unit + "/s"
                        case "Z":
                            decoded += ", Z Jerk: " + value + " " + printer.unit + "/s"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M221: Set extrude factor override percentage
            case "M221":
                decoded = ""
                if metaInfos.generator != "Slic3r" and metaInfos.generator != "PrusaSlicer":
                    decoded = self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded += "Set extrude factor override percentage"
                        case "S":
                            decoded += ", Extrude factor override percentage: " + value + " %"
                            # TODO: What is this doing exactly?
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M300: Play beep sound
            case "M300":
                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded = "Play beep sound"
                        case "P":
                            decoded += ", duration: " + value + " ms"
                        case "S":
                            decoded += ", frequency: " + value + " Hz"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M862.1: Check nozzle diameter (prusa only)
            case "M862.1":
                decoded = ""
                if metaInfos.generator != "PrusaSlicer":
                    decoded = self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                return decoded + "Check nozzle diameter (prusa only, undecoded): " + str(splitted)
            # M862.3: Model name (prusa only)
            case "M862.3":
                decoded = ""
                if metaInfos.generator != "PrusaSlicer":
                    decoded = self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                return decoded + "Model name (prusa only, undecoded): " + str(splitted)
            # M900 Set Linear Advance Scaling Factors
            # https://marlinfw.org/docs/features/lin_advance.html
            case "M900":
                decoded = ""
                if metaInfos.generator != "Slic3r" and metaInfos.generator != "PrusaSlicer":
                    decoded = self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "M":
                            decoded += "Set Linear Advance Scaling Factors"
                        case "K":
                            decoded += ", Advance K factor: " + value
                            # TODO: What is this doing exactly?
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded
            # M907: Set digital trimpot motor current
            case "M907":
                decoded = ""
                if metaInfos.generator != "PrusaSlicer":
                    decoded = self.error_firmwareDependentButUnknownGenerator(metaInfos, splitted) + " "

                for token in splitted:
                    key = token[0]
                    value = token[1:]
                    match key:
                        case "E":
                            if float(value) <= 2.50:
                                unit = "A"
                            elif float(value) <= 200:
                                unit = "%"
                            elif float(value) <= 2500:
                                unit = "mA"
                            else:
                                decoded += self.error_valueOutOfRange(line, value)
                                unit = "?"
                            decoded += ", Set E stepper current: " + value + " " + unit
                        case "M":
                            decoded += "Set digital trimpot motor current"
                        case _:
                            decoded += self.error_undecodedGCodeSubtoken(splitted, token)
                return decoded

            case _:
                return self.error_undecodedGCode(line)
