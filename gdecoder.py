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


def get_diff(value_high, value_low):
    if value_high != "?" and value_low != "?":
        diff_x_float = round(float(value_high) - float(value_low), 2)
        return str(diff_x_float)
    else:
        return "?"


def print_printer_model(printer):
    diff_x = get_diff(printer.print_position_x.get_max(), printer.print_position_x.get_min())
    diff_y = get_diff(printer.print_position_y.get_max(), printer.print_position_y.get_min())
    diff_z = get_diff(printer.print_position_z.get_max(), printer.print_position_z.get_min())
    e_phys = round(float(printer.extruder_physical.get()), 2)
    e_phys_max = round(float(printer.extruder_physical.get_max()), 2)
    e_log = round(float(printer.extruder_logical.get()), 2)

    print(";------------------------------------------------------------------------------")
    print(";X: " + printer.print_position_x.get() + " " + printer.unit, end="")
    print(f" (min: {printer.print_position_x.get_min()} max: {printer.print_position_x.get_max()} diff: {diff_x})")

    print(";Y: " + printer.print_position_y.get() + " " + printer.unit, end="")
    print(f" (min: {printer.print_position_y.get_min()} max: {printer.print_position_y.get_max()} diff: {diff_y})")

    print(";Z: " + printer.print_position_z.get() + " " + printer.unit, end="")
    print(f" (min: {printer.print_position_z.get_min()} max: {printer.print_position_z.get_max()} diff: {diff_z})")

    print(";E: " + str(e_log) + " " + printer.unit, end="")
    print(" (phys: " + str(e_phys) + ", max: " + str(e_phys_max) + ", move mode: " + printer.extruder_move_mode + ")")

    print(";Feedrate: " + printer.feedrate + " " + printer.unit + "/min")

    print(";Temperature: Extruder: " + printer.extruder_temp.get() + " °C", end="")
    print(", bed: " + printer.bed_temp.get() + " °C", end="")
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


def print_filament_infos(filament, length):
    material = filament[0]
    meter_per_kg_min = filament[1]
    meter_per_kg_max = filament[2]
    weight_min = round(length / meter_per_kg_max, 1)
    weight_max = round(length / meter_per_kg_min, 1)
    price_per_kg_min = filament[3]
    price_per_kg_max = filament[4]
    price_min = round(weight_min * price_per_kg_min / 1000, 2)
    price_max = round(weight_max * price_per_kg_max / 1000, 2)
    nozzle_min = filament[5]
    nozzle_max = filament[6]
    bed_min = filament[7]
    bed_max = filament[8]
    bed_mandatory = filament[9]

    weight = str(weight_min) + "-" + str(weight_max) + " g"
    price = str(price_min) + "-" + str(price_max) + " €"
    print(";  " + material + "     : " + weight + ", " + price, end="")

    print("    1.75 mm/1kg: Length:", end="")
    print(" " + str(meter_per_kg_min) + "-" + str(meter_per_kg_max) + " m/kg", end="")
    print(", Price: " + str(price_per_kg_min) + "-" + str(price_per_kg_max) + " €/kg", end="")
    print(", Nozzle: " + str(nozzle_min) + "-" + str(nozzle_max) + " °C", end="")
    print(", Bed: " + str(bed_min) + "-" + str(bed_max) + " °C", end="")
    if not bed_mandatory:
        print(" (bed optional)")
    else:
        print("")


def is_filament_suitable_for_temp(filament, temp_nozzle, temp_bed):
    nozzle_min = filament[5]
    nozzle_max = filament[6]
    bed_min = filament[7]
    bed_max = filament[8]
    bed_mandatory = filament[9]

    if temp_nozzle.isdigit():
        temp_nozzle_int = int(temp_nozzle)
    else:
        temp_nozzle_int = 0
    if temp_bed.isdigit():
        temp_bed_int = int(temp_bed)
    else:
        temp_bed_int = 0

    # check nozzle temp
    if temp_nozzle_int < nozzle_min or temp_nozzle_int > nozzle_max:
        return False

    # check bed temp
    if (bed_mandatory and temp_bed_int < bed_min) or temp_bed_int > bed_max:
        return False

    return True


def print_summary_infos(meta_infos, printer, gcode_command_count):
    diff_x = get_diff(printer.print_position_x.get_max(), printer.print_position_x.get_min())
    diff_y = get_diff(printer.print_position_y.get_max(), printer.print_position_y.get_min())
    diff_z = get_diff(printer.print_position_z.get_max(), printer.print_position_z.get_min())

    print(";------------------------------------------------------------------------------")
    print(";Summary:")
    print(";File")
    print(";  Name      : " + meta_infos.file_name)
    print(";  Size      : " + str(meta_infos.file_size) + " bytes")
    print(";  Modified  : %s" % time.ctime(meta_infos.modified_time))
    print(";  Lines     : " + str(meta_infos.line_count))
    print(";  Longest   : " + str(meta_infos.longest_line) + " characters (without comment lines)")
    print(";  GCode     : " + str(gcode_command_count) + " commands")
    generator_line = meta_infos.generator_line.strip(";")
    print(";Generator")
    print(";  Line      : " + generator_line.strip())
    print(";  Name      : " + meta_infos.generator)
    print(";  Flavor    : " + meta_infos.generator_flavor)
    print(";Printed")
    print(";  X         : " + diff_x + " " + printer.unit)
    print(";  Y         : " + diff_y + " " + printer.unit)
    print(";  Z         : " + diff_z + " " + printer.unit)
    print(";Temperature")
    print(";  Extruder  : " + printer.extruder_temp.get_max() + " °C (max.)")
    print(";  Bed       : " + printer.bed_temp.get_max() + " °C (max.)")
    print(";  Fan       : " + printer.fan.get_max() + " (max.)")

    e_phys_max = round(float(printer.extruder_physical.get_max()), 2)
    print(";Filament")
    print(";  Length    : " + str(e_phys_max) + " " + printer.unit)

    print(";  suitable")
    for filament in filaments:
        if is_filament_suitable_for_temp(filament, printer.extruder_temp.get_max(), printer.bed_temp.get_max()):
            print_filament_infos(filament, e_phys_max)

    print(";  unsuitable")
    for filament in filaments:
        if not is_filament_suitable_for_temp(filament, printer.extruder_temp.get_max(), printer.bed_temp.get_max()):
            print_filament_infos(filament, e_phys_max)

    # TODO: Add Time, Energy costs


def read_gcode(args, meta_infos, decode_line, printer):
    file1 = open(args.input, 'r', encoding='utf-8')
    lines = file1.readlines()
    gcode_command_count = 0

    for line in lines:
        line = line.strip()

        # comment line?
        if line.startswith(";"):
            # reset z value, caused by extruder initial cleanup procedure (at least on Cura/Marlin and PrusaSlicer)
            if ";TYPE:SKIRT".lower() in line.lower():
                current_z = printer.position_z.get()
                printer.print_position_z.set(current_z)

            if args.hideComments is False:
                print(line)
            continue

        decoded = decode_line.decode_gcode_line(meta_infos, line, printer)

        if decoded != "":
            gcode_command_count += 1

        if args.hideGCode is False:
            formatstr = "{:" + str(meta_infos.longest_line + 1) + "}"
            print(formatstr.format(line.strip()), end="")

        if args.hideDecoded is False and decoded != "":
            print(' ; ' + decoded)
        else:
            if args.hideGCode is False:
                print()

        if args.showVerbose is True:
            print_printer_model(printer)

    return gcode_command_count


def gdecoder(args):
    printer = PrinterModel()

    meta_infos = FileMetaInfos()
    meta_infos.read_meta_infos(args.input)

    decode_line = GDecoderLine()
    decode_line.stop_on_undecoded = args.stopOnUndecoded

    gcode_command_count = read_gcode(args, meta_infos, decode_line, printer)

    if args.hideSummary is False:
        print_summary_infos(meta_infos, printer, gcode_command_count)


def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # TODO: use stdin as default
    parser.add_argument('--input', '-i',
                        help='input gcode file', required="True")
    parser.add_argument('--summary', '-s',
                        help='hide summary', action='store_true', dest="hideSummary")
    parser.add_argument('--comments', '-c',
                        help='hide original gcode comments', action='store_true', dest="hideComments")
    parser.add_argument('--gcode', '-g',
                        help='hide original gcode commands', action='store_true', dest="hideGCode")
    parser.add_argument('--decoded', '-d',
                        help='hide gcode decoded output', action='store_true', dest="hideDecoded")
    parser.add_argument('--verbose', '-v',
                        help='show verbose output (can be slow!)', action='store_true', dest="showVerbose")
    parser.add_argument('--undecoded', '-u',
                        help='stop on undecoded gcode', action='store_true', dest="stopOnUndecoded")
    return parser.parse_args(args)


if __name__ == '__main__':
    parser = parse_args(sys.argv[1:])
    gdecoder(parser)
