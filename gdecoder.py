# Simple decode of gcode 3D printer files
# focussed on common x/y/z printer with a single extruder
#
# Hint: Many gcode details can be found at:
# https://reprap.org/wiki/G-code
# https://marlinfw.org/meta/gcode/

from PrinterModel import PrinterModel
from FileMetaInfos import FileMetaInfos
import argparse
import time


stopOnUndecoded = False


def undecodedGCodeSubtoken(splitted, token):
    message = "Unknown subtoken: " + token + " in: " + str(splitted)
    if stopOnUndecoded:
        raise Exception(message)
    else:
        return message


def firmwareDependentButUnknownGenerator(metaInfos, splitted):
    message = "Uexpected generator " + metaInfos.generator_line + " for firmware dependent: " + str(splitted)
    if stopOnUndecoded:
        raise Exception(message)
    else:
        return message


def decodeGCodeLine(metaInfos, line, printer):
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
                        decoded += ", Feedrate: " + value + " " + printer.unit + "/min."
                        printer.setFeedrate(value)
                    case "G":
                        decoded = "Rapid Move"
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += ", Feedrate: " + value + " " + printer.unit + "/min."
                        printer.setFeedrate(value)
                    case "G":
                        decoded = "Linear Move"
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += ", feedrate/min.: " + value
                        printer.setFeedrate(value)
                    case "G":
                        decoded = "Clockwise Arc Move"
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += ", feedrate/min.: " + value
                        printer.setFeedrate(value)
                    case "G":
                        decoded = "Counter-Clockwise Arc Move"
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # G21: Set Units to Millimeters
        case "G21":
            for token in splitted:
                key = token[0]
                match key:
                    case "G":
                        decoded = "Set Units to Millimeters"
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)

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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # G92: Set Position
        case "G92":
            for token in splitted:
                key = token[0]
                value = token[1:]
                match key:
                    case "E":
                        decoded += ", new extruder position: " + value
                        printer.setExtruderPosition(value)
                    case "G":
                        decoded = "Set Position"
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded = "Normal mode: " + value + " %"
                    case "Q":
                        decoded = "Silent mode: " + value + " %"
                    case "R":
                        decoded = "Remaining in normal mode: " + value + " min."
                    case "S":
                        decoded = "Remaining in silent mode: " + value + " min."
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # M84: Stop idle hold
        case "M84":
            for token in splitted:
                key = token[0]
                value = token[1:]
                match key:
                    case "M":
                        decoded = "Stop idle hold"
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += ", Fan Speed: " + value
                        printer.setFan(value)
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # M117: Display Message
        case "M117":
            decoded = "Display Message: " + line[5:]
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # M203: Firmware dependent
        case "M203":
            if metaInfos.generator != "PrusaSlicer":
                firmwareDependentButUnknownGenerator(metaInfos, splitted)

            # M203: Set maximum feedrate
            for token in splitted:
                key = token[0]
                value = token[1:]
                match key:
                    case "E":
                        decoded += ", E: " + value + " " + printer.unit + "/s²"
                    case "M":
                        decoded = "Set maximum feedrate"
                    case "X":
                        decoded += ", X: " + value + " " + printer.unit + "/s²"
                    case "Y":
                        decoded += ", Y: " + value + " " + printer.unit + "/s²"
                    case "Z":
                        decoded += ", Z: " + value + " " + printer.unit + "/s²"
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # M204: Firmware dependent
        # https://reprap.org/wiki/G-code#M204:_Firmware_dependent
        case "M204":
            if metaInfos.generator != "PrusaSlicer" and metaInfos.generator != "Cura" and metaInfos.generator != "Slic3r":
                firmwareDependentButUnknownGenerator(splitted)

            if metaInfos.generator == "Cura" and metaInfos.generator_flavor != "Marlin":
                firmwareDependentButUnknownGenerator(splitted)

            # M204: Set default acceleration
            for token in splitted:
                key = token[0]
                value = token[1:]
                match key:
                    case "M":
                        decoded = "Set default acceleration"
                    case "P":
                        decoded += ", printing: " + value + " " + printer.unit + "/s²"
                    case "R":
                        decoded += ", retract: " + value + " " + printer.unit + "/s²"
                    case "S":
                        decoded += ", normal: " + value + " " + printer.unit + "/s²"
                    case "T":
                        decoded += ", travel: " + value + " " + printer.unit + "/s²"
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # M205: Firmware dependent
        # https://reprap.org/wiki/G-code#M205:_Firmware_dependent
        case "M205":
            if metaInfos.generator != "PrusaSlicer" and metaInfos.generator != "Cura":
                firmwareDependentButUnknownGenerator(splitted)

            if metaInfos.generator == "Cura" and metaInfos.generator_flavor != "Marlin":
                firmwareDependentButUnknownGenerator(splitted)

            # M205: Advanced Settings
            for token in splitted:
                key = token[0]
                value = token[1:]
                match key:
                    case "E":
                        decoded += ", E jerk: " + value + " " + printer.unit + "/s"
                    case "M":
                        decoded = "Advanced settings"
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # M221: Set extrude factor override percentage
        case "M221":
            if metaInfos.generator != "Slic3r" and metaInfos.generator != "PrusaSlicer":
                firmwareDependentButUnknownGenerator(splitted)

            for token in splitted:
                key = token[0]
                value = token[1:]
                match key:
                    case "M":
                        decoded = "Set extrude factor override percentage"
                    case "S":
                        decoded += ", Extrude factor override percentage: " + value + " %"
                        # TODO: What is this doing exactly?
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
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
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # M862.1: Check nozzle diameter (prusa only)
        case "M862.1":
            if metaInfos.generator != "PrusaSlicer":
                firmwareDependentButUnknownGenerator(splitted)

            return "Check nozzle diameter (prusa only, undecoded): " + str(splitted)
        # M862.3: Model name (prusa only)
        case "M862.3":
            if metaInfos.generator != "PrusaSlicer":
                firmwareDependentButUnknownGenerator(splitted)

            return "Model name (prusa only, undecoded): " + str(splitted)
        # M900 Set Linear Advance Scaling Factors
        # https://marlinfw.org/docs/features/lin_advance.html
        case "M900":
            if metaInfos.generator != "Slic3r" and metaInfos.generator != "PrusaSlicer":
                firmwareDependentButUnknownGenerator(splitted)

            for token in splitted:
                key = token[0]
                value = token[1:]
                match key:
                    case "M":
                        decoded = "Set Linear Advance Scaling Factors"
                    case "K":
                        decoded += ", Advance K factor: " + value
                        # TODO: What is this doing exactly?
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded
        # M907: Set digital trimpot motor current
        case "M907":
            if metaInfos.generator != "PrusaSlicer":
                firmwareDependentButUnknownGenerator(splitted)

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
                            raise Exception("M907: Invalid value range: " + str(splitted))
                        decoded += ", Set E stepper current: " + value + " " + unit
                    case "M":
                        decoded = "Set digital trimpot motor current"
                    case _:
                        decoded += undecodedGCodeSubtoken(splitted, token)
            return decoded

        case _:
            # raise Exception("Unknown gcode command: " + str(splitted))
            print("unknown gcode: " + str(splitted))
            return "unknown gcode: " + str(splitted)


def getDiff(valueHigh, valueLow):
    if valueHigh != "?" and valueLow != "?":
        diffXFloat = round(float(valueHigh) - float(valueLow), 2)
        return str(diffXFloat)
    else:
        return "?"


def printModelInfos(printer):
    diffX = getDiff(printer.printPositionX.getMax(), printer.printPositionX.getMin())
    diffY = getDiff(printer.printPositionY.getMax(), printer.printPositionY.getMin())
    diffZ = getDiff(printer.printPositionZ.getMax(), printer.printPositionZ.getMin())
    ePhys = round(float(printer.extruderPhysical.get()), 2)
    ePhysMax = round(float(printer.extruderPhysical.getMax()), 2)
    eLog = round(float(printer.extruderLogical.get()), 2)

    print(";------------------------------------------------------------------------------")
    print(";X: " + printer.positionX.get() + " " + printer.unit, end="")
    print(" (min: " + printer.positionX.getMin() + " max: " + printer.positionX.getMax() + " diff: " + diffX + ")")

    print(";Y: " + printer.positionY.get() + " " + printer.unit, end="")
    print(" (min: " + printer.printPositionY.getMin() + " max: " + printer.printPositionY.getMax() + " diff: " + diffY + ")")

    print(";Z: " + printer.positionZ.get() + " " + printer.unit, end="")
    print(" (min: " + printer.printPositionZ.getMin() + " max: " + printer.printPositionZ.getMax() + " diff: " + diffZ + ")")

    print(";E: " + str(eLog) + " " + printer.unit, end="")
    print(" (phys: " + str(ePhys) + ", max: " + str(ePhysMax) + ", move mode: " + printer.extruderMoveMode + ")")

    print(";Feedrate: " + printer.feedrate + " " + printer.unit + "/min")

    print(";Temperature: Extruder: " + printer.extruderTemp.get() + " °C", end="")
    print(", bed: " + printer.bedTemp.get() + " °C", end="")
    print(", fan: " + printer.fan.get() + " (0-255)")
    print(";------------------------------------------------------------------------------")


filaments = [
    # rough filament infos from a quick research (2023.12)
    # material, m/kg min, m/kg max, price/kg min, price/kg max, nozzleMin, nozzleMax, bedMin, bedMax, bedMandatory
    ["PLA  ", 325, 340, 15, 30, 180, 230, 20, 80, False],
    ["PETG ", 310, 350, 17, 30, 220, 250, 50, 90, False],
    ["ABS  ", 380, 405, 15, 30, 230, 270, 80, 110, True],
    ["Nylon", 330, 360, 23, 50, 220, 290, 85, 120, True],
    ["TPU  ", 330, 360, 17, 50, 190, 260, 25, 70, True]
]


def printFilamentInfos(filament, length):
    material = filament[0]
    meterPerKgMin = filament[1]
    meterPerKgMax = filament[2]
    weightMin = round(length / meterPerKgMax, 1)
    weightMax = round(length / meterPerKgMin, 1)
    pricePerKgMin = filament[3]
    pricePerKgMax = filament[4]
    priceMin = round(weightMin * pricePerKgMin / 1000, 2)
    priceMax = round(weightMax * pricePerKgMax / 1000, 2)
    nozzleMin = filament[5]
    nozzleMax = filament[6]
    bedMin = filament[7]
    bedMax = filament[8]
    bedMandatory = filament[9]

    weight = str(weightMin) + "-" + str(weightMax) + " g"
    price = str(priceMin) + "-" + str(priceMax) + " €"
    print(";  " + material + "     : " + weight + ", " + price, end="")

    print("    1.75 mm/1kg: Length:", end="")
    print(" " + str(meterPerKgMin) + "-" + str(meterPerKgMax) + " m/kg", end="")
    print(", Price: " + str(pricePerKgMin) + "-" + str(pricePerKgMax) + " €/kg", end="")
    print(", Nozzle: " + str(nozzleMin) + "-" + str(nozzleMax) + " °C", end="")
    print(", Bed: " + str(bedMin) + "-" + str(bedMax) + " °C", end="")
    if not bedMandatory:
        print(" (bed optional)")
    else:
        print("")


def isFilamentSuitableForTemp(filament, tempNozzle, tempBed):
    nozzleMin = filament[5]
    nozzleMax = filament[6]
    bedMin = filament[7]
    bedMax = filament[8]
    bedMandatory = filament[9]

    tempNozzleInt = int(tempNozzle)
    tempBedInt = int(tempBed)

    # check nozzle temp
    if tempNozzleInt < nozzleMin or tempNozzleInt > nozzleMax:
        return False

    # check bed temp
    if (bedMandatory and tempBedInt < bedMin) or tempBedInt > bedMax:
        return False

    return True


def printSummaryInfos(metaInfos, printer, gcodeCommandCount):
    diffX = getDiff(printer.printPositionX.getMax(), printer.printPositionX.getMin())
    diffY = getDiff(printer.printPositionY.getMax(), printer.printPositionY.getMin())
    diffZ = getDiff(printer.printPositionZ.getMax(), printer.printPositionZ.getMin())

    print(";------------------------------------------------------------------------------")
    print(";Summary:")
    print(";File")
    print(";  Name      : " + metaInfos.fileName)
    print(";  Size      : " + str(metaInfos.fileSize) + " bytes")
    print(";  Modified  : %s" % time.ctime(metaInfos.modifiedTime))
    print(";  Lines     : " + str(metaInfos.lineCount))
    print(";  Longest   : " + str(metaInfos.longestLine) + " characters (without comment lines)")
    print(";  GCode     : " + str(gcodeCommandCount) + " commands")
    generator_line = metaInfos.generator_line.strip(";")
    print(";Generator")
    print(";  Line      : " + generator_line.strip())
    print(";  Name      : " + metaInfos.generator)
    print(";  Flavor    : " + metaInfos.generator_flavor)
    print(";Printed")
    print(";  X         : " + diffX + " " + printer.unit)
    print(";  Y         : " + diffY + " " + printer.unit)
    print(";  Z         : " + diffZ + " " + printer.unit)
    print(";Temperature")
    print(";  Extruder  : " + printer.extruderTemp.getMax() + " °C (max.)")
    print(";  Bed       : " + printer.bedTemp.getMax() + " °C (max.)")
    print(";  Fan       : " + printer.fan.getMax() + " (max.)")

    ePhysMax = round(float(printer.extruderPhysical.getMax()), 2)
    print(";Filament")
    print(";  Length    : " + str(ePhysMax) + " " + printer.unit)

    print(";  suitable")
    for filament in filaments:
        if isFilamentSuitableForTemp(filament, printer.extruderTemp.getMax(), printer.bedTemp.getMax()):
            printFilamentInfos(filament, ePhysMax)

    print(";  unsuitable")
    for filament in filaments:
        if not isFilamentSuitableForTemp(filament, printer.extruderTemp.getMax(), printer.bedTemp.getMax()):
            printFilamentInfos(filament, ePhysMax)

    # TODO: Add Time, Energy costs


def readGCode(args, metaInfos, printer):
    file1 = open(args.input, 'r', encoding='utf-8')
    Lines = file1.readlines()
    gcodeCommandCount = 0

    for line in Lines:
        line = line.strip()

        # comment line?
        if line.startswith(";"):
            # reset z value, caused by extruder initial cleanup procedure (at least on Cura/Marlin and PrusaSlicer)
            if ";TYPE:SKIRT".lower() in line.lower():
                currentZ = printer.positionZ.get()
                printer.printPositionZ.set(currentZ)

            if args.hideComments is False:
                print(line)
            continue

        decoded = decodeGCodeLine(metaInfos, line, printer)

        if decoded != "":
            gcodeCommandCount += 1

        if args.hideGCode is False:
            formatstr = "{:" + str(metaInfos.longestLine + 1) + "}"
            print(formatstr.format(line.strip()), end="")

        if args.hideDecoded is False:
            print(' ; ' + decoded)
        else:
            if args.hideGCode is False:
                print()

        if args.showVerbose is True:
            printModelInfos(printer)

    return gcodeCommandCount


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # TODO: use stdin as default
    parser.add_argument('--input', '-i', help='input gcode file', required="True")
    parser.add_argument('--summary', '-s', help='hide summary', action='store_true', dest="hideSummary")
    parser.add_argument('--comments', '-c', help='hide original gcode comments', action='store_true', dest="hideComments")
    parser.add_argument('--gcode', '-g', help='hide original gcode commands', action='store_true', dest="hideGCode")
    parser.add_argument('--decoded', '-d', help='hide gcode decoded output', action='store_true', dest="hideDecoded")
    parser.add_argument('--verbose', '-v', help='show verbose output (can be slow!)', action='store_true', dest="showVerbose")
    parser.add_argument('--undecoded', '-u', help='stop on undecoded gcode', action='store_true', dest="stopOnUndecoded")
    args = parser.parse_args()

    stopOnUndecoded = args.stopOnUndecoded

    printer = PrinterModel()

    metaInfos = FileMetaInfos()
    metaInfos.readMetaInfos(args.input)

    gcodeCommandCount = readGCode(args, metaInfos, printer)

    if args.hideSummary is False:
        printSummaryInfos(metaInfos, printer, gcodeCommandCount)
