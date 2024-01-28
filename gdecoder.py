# Simple decode of gcode 3D printer files
# focused on common x/y/z printer with a single extruder
#
# Hint: Many gcode details can be found at:
# https://reprap.org/wiki/G-code
# https://marlinfw.org/meta/gcode/

from PrinterModel import PrinterModel
from FileMetaInfos import FileMetaInfos
from GDecoderLine import GDecoderLine
import argparse
import time
import sys


def getDiff(valueHigh, valueLow):
    if valueHigh != "?" and valueLow != "?":
        diffXFloat = round(float(valueHigh) - float(valueLow), 2)
        return str(diffXFloat)
    else:
        return "?"


def printPrinterModel(printer):
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

    if tempNozzle.isdigit():
        tempNozzleInt = int(tempNozzle)
    else:
        tempNozzleInt = 0
    if tempBed.isdigit():
        tempBedInt = int(tempBed)
    else:
        tempBedInt = 0

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


def readGCode(args, metaInfos, decodeLine, printer):
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

        decoded = decodeLine.decodeGCodeLine(metaInfos, line, printer)

        if decoded != "":
            gcodeCommandCount += 1

        if args.hideGCode is False:
            formatstr = "{:" + str(metaInfos.longestLine + 1) + "}"
            print(formatstr.format(line.strip()), end="")

        if args.hideDecoded is False and decoded != "":
            print(' ; ' + decoded)
        else:
            if args.hideGCode is False:
                print()

        if args.showVerbose is True:
            printPrinterModel(printer)

    return gcodeCommandCount


def gdecoder(args):
    printer = PrinterModel()

    metaInfos = FileMetaInfos()
    metaInfos.readMetaInfos(args.input)

    decodeLine = GDecoderLine()
    decodeLine.stopOnUndecoded = args.stopOnUndecoded

    gcodeCommandCount = readGCode(args, metaInfos, decodeLine, printer)

    if args.hideSummary is False:
        printSummaryInfos(metaInfos, printer, gcodeCommandCount)


def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # TODO: use stdin as default
    parser.add_argument('--input', '-i', help='input gcode file', required="True")
    parser.add_argument('--summary', '-s', help='hide summary', action='store_true', dest="hideSummary")
    parser.add_argument('--comments', '-c', help='hide original gcode comments', action='store_true', dest="hideComments")
    parser.add_argument('--gcode', '-g', help='hide original gcode commands', action='store_true', dest="hideGCode")
    parser.add_argument('--decoded', '-d', help='hide gcode decoded output', action='store_true', dest="hideDecoded")
    parser.add_argument('--verbose', '-v', help='show verbose output (can be slow!)', action='store_true', dest="showVerbose")
    parser.add_argument('--undecoded', '-u', help='stop on undecoded gcode', action='store_true', dest="stopOnUndecoded")
    return parser.parse_args(args)


if __name__ == '__main__':
    parser = parse_args(sys.argv[1:])
    gdecoder(parser)
