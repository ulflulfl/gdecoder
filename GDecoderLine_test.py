from GDecoderLine import GDecoderLine
from PrinterModel import PrinterModel
from FileMetaInfos import FileMetaInfos
import pytest
pytestmark = pytest.mark.unittests


gcode_empty_testdata = [
    ("", ""),
    ("Filament-specific end gcode", ""),    # ignore a slicer bug
]


@pytest.mark.parametrize("gcode,expected_decode", gcode_empty_testdata)
def test_decode_gcode_line_empty_output(gcode, expected_decode):
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, gcode, printer)

    # assert
    assert(decoded) == expected_decode


invalid_gcode_testdata = [
    ("invalid", "", "Unknown gcode: invalid"),
    ("G0 invalidCommand", "Rapid Move (no print), ",
        "Unknown subtoken: invalidCommand in: ['G0', 'invalidCommand']"),
    ("G1 invalidCommand", "Linear Move (print), ",
        "Unknown subtoken: invalidCommand in: ['G1', 'invalidCommand']"),
    ("G2 invalidCommand", "Clockwise Arc Move (print), ",
        "Unknown subtoken: invalidCommand in: ['G2', 'invalidCommand']"),
    ("G3 invalidCommand", "Counter-Clockwise Arc Move (print), ",
        "Unknown subtoken: invalidCommand in: ['G3', 'invalidCommand']"),
    ("G4 invalidCommand", "Dwell (aka: Pause), ",
        "Unknown subtoken: invalidCommand in: ['G4', 'invalidCommand']"),
    ("G21 invalidCommand", "Set Units to Millimeters, ",
        "Unknown subtoken: invalidCommand in: ['G21', 'invalidCommand']"),
    ("G28 invalidCommand", "Move to Origin (Home, often: X=0, Y=0; Z=0), ",
        "Unknown subtoken: invalidCommand in: ['G28', 'invalidCommand']"),
    ("G80 invalidCommand", "Mesh-based Z probe, ",
        "Unknown subtoken: invalidCommand in: ['G80', 'invalidCommand']"),
    ("G90 invalidCommand", "Set to Absolute Positioning, ",
        "Unknown subtoken: invalidCommand in: ['G90', 'invalidCommand']"),
    ("G91 invalidCommand", "Set to Relative Positioning, ",
        "Unknown subtoken: invalidCommand in: ['G91', 'invalidCommand']"),
    ("G92 invalidCommand", "Set Position, ",
        "Unknown subtoken: invalidCommand in: ['G92', 'invalidCommand']"),
    ("M73 invalidCommand", "Set/Get build percentage, ",
        "Unknown subtoken: invalidCommand in: ['M73', 'invalidCommand']"),
    ("M82 invalidCommand", "Set extruder to absolute mode, ",
        "Unknown subtoken: invalidCommand in: ['M82', 'invalidCommand']"),
    ("M83 invalidCommand", "Set extruder to relative mode, ",
        "Unknown subtoken: invalidCommand in: ['M83', 'invalidCommand']"),
    ("M84 invalidCommand", "Stop idle hold (disable motors), ",
        "Unknown subtoken: invalidCommand in: ['M84', 'invalidCommand']"),
    ("M104 invalidCommand", "Set Extruder Temperature, ",
        "Unknown subtoken: invalidCommand in: ['M104', 'invalidCommand']"),
    ("M105 invalidCommand", "Get Extruder Temperature, ",
        "Unknown subtoken: invalidCommand in: ['M105', 'invalidCommand']"),
    ("M106 invalidCommand", "Fan On, ",
        "Unknown subtoken: invalidCommand in: ['M106', 'invalidCommand']"),
    ("M107 invalidCommand", "Fan Off, ",
        "Unknown subtoken: invalidCommand in: ['M107', 'invalidCommand']"),
    ("M109 invalidCommand", "Set Extruder Temperature and Wait, ",
        "Unknown subtoken: invalidCommand in: ['M109', 'invalidCommand']"),
    ("M115 invalidCommand", "Get Firmware Version and Capabilities, ",
        "Unknown subtoken: invalidCommand in: ['M115', 'invalidCommand']"),
    ("M140 invalidCommand", "Set Bed Temperature (Fast), ",
        "Unknown subtoken: invalidCommand in: ['M140', 'invalidCommand']"),
    ("M190 invalidCommand", "Wait for bed temperature to reach target temp, ",
        "Unknown subtoken: invalidCommand in: ['M190', 'invalidCommand']"),
    ("M201 invalidCommand", "Set max acceleration, ",
        "Unknown subtoken: invalidCommand in: ['M201', 'invalidCommand']"),
    ("M300 invalidCommand", "Play beep sound, ",
        "Unknown subtoken: invalidCommand in: ['M300', 'invalidCommand']"),
]


@pytest.mark.parametrize("gcode,expected_decode,expected_message", invalid_gcode_testdata)
def test_decode_gcode_line_invalid_command_error_message(gcode, expected_decode, expected_message):
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, gcode, printer)

    # assert
    assert(decoded) == expected_decode + expected_message


@pytest.mark.parametrize("gcode,expected_decode,expected_message", invalid_gcode_testdata)
def test_decode_gcode_line_invalid_command_raises_exception(gcode, expected_decode, expected_message):
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    decode_line = GDecoderLine()
    decode_line.stop_on_undecoded = True

    # act
    with pytest.raises(Exception) as e_info:
        decode_line.decode_gcode_line(meta_infos, gcode, printer)

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == expected_message


generator_specific_gcode_testdata = [
    ("M203 X1 Y2 Z3 E4", "PrusaSlicer",
        "Set maximum feedrate, X: 1 mm/s², Y: 2 mm/s², Z: 3 mm/s², E: 4 mm/s²"),
    ("M203 invalidCommand",
        "PrusaSlicer", "Set maximum feedrate, Unknown subtoken: invalidCommand in: ['M203', 'invalidCommand']"),
    ("M204 P1 R2 S3 T4",
        "PrusaSlicer", "Set default acceleration, "
        "printing: 1 mm/s², retract: 2 mm/s², normal: 3 mm/s², travel: 4 mm/s²"),
    ("M204 invalidCommand",
        "PrusaSlicer", "Set default acceleration, Unknown subtoken: invalidCommand in: ['M204', 'invalidCommand']"),
    ("M205 X1 Y2 Z3 S4 T5 E6",
        "PrusaSlicer", "Advanced settings, X Jerk: 1 mm/s, Y Jerk: 2 mm/s, Z Jerk: 3 mm/s, "
        "min. print speed: 4 mm/s, min. travel speed: 5 mm/s, E jerk: 6 mm/s"),
    ("M205 invalidCommand",
        "PrusaSlicer", "Advanced settings, Unknown subtoken: invalidCommand in: ['M205', 'invalidCommand']"),
    ("M221 S1", "PrusaSlicer",
        "Set extrude factor override percentage, Extrude factor override percentage: 1 %"),
    ("M221 invalidCommand",
        "PrusaSlicer", "Set extrude factor override percentage, "
        "Unknown subtoken: invalidCommand in: ['M221', 'invalidCommand']"),
    ("M900 K1", "PrusaSlicer",
        "Set Linear Advance Scaling Factors, Advance K factor: 1"),
    ("M900 invalidCommand",
        "PrusaSlicer", "Set Linear Advance Scaling Factors, "
        "Unknown subtoken: invalidCommand in: ['M900', 'invalidCommand']"),
    ("M907 E1", "PrusaSlicer",
        "Set digital trimpot motor current, Set E stepper current: 1 A"),
    ("M907 E100", "PrusaSlicer",
        "Set digital trimpot motor current, Set E stepper current: 100 %"),
    ("M907 E1000", "PrusaSlicer",
        "Set digital trimpot motor current, Set E stepper current: 1000 mA"),
    ("M907 E10000", "PrusaSlicer",
        "Set digital trimpot motor current, Value 10000 out of range in: M907 E10000, Set E stepper current: 10000 ?"),
    ("M907 invalidCommand", "PrusaSlicer",
        "Set digital trimpot motor current, Unknown subtoken: invalidCommand in: ['M907', 'invalidCommand']"),
]


@pytest.mark.parametrize("gcode,generator,expected_message", generator_specific_gcode_testdata)
def test_decode_gcode_line_generator_specific_message(gcode, generator, expected_message):
    # arrange
    meta_infos = FileMetaInfos()
    meta_infos.generator = generator
    printer = PrinterModel()
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, gcode, printer)

    # assert
    assert(decoded) == expected_message


def test_decode_gcode_line_generator_specific_out_of_range_raises_exception():
    # arrange
    meta_infos = FileMetaInfos()
    meta_infos.generator = "PrusaSlicer"
    printer = PrinterModel()
    decode_line = GDecoderLine()
    decode_line.stop_on_undecoded = True

    # act
    with pytest.raises(Exception) as e_info:
        decode_line.decode_gcode_line(meta_infos, "M907 E10000", printer)

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "Value 10000 out of range in: M907 E10000"


generator_specific_gcode_wrong_generator_testdata = [
    ("M203", "", "['M203'] Set maximum feedrate"),
    ("M203", "Cura", "['M203'] Set maximum feedrate"),
    ("M203", "Slic3r", "['M203'] Set maximum feedrate"),
    ("M204", "", "['M204'] Set default acceleration"),
    ("M204", "Cura", "['M204'] Set default acceleration"),
    ("M205", "", "['M205'] Advanced settings"),
    ("M205", "Slic3r", "['M205'] Advanced settings"),
    ("M205", "Cura", "['M205'] Advanced settings"),
    ("M221", "", "['M221'] Set extrude factor override percentage"),
    ("M221", "Cura", "['M221'] Set extrude factor override percentage"),
    ("M862.1", "", "['M862.1'] Check nozzle diameter (prusa only, undecoded): ['M862.1']"),
    ("M862.1", "Slic3r", "['M862.1'] Check nozzle diameter (prusa only, undecoded): ['M862.1']"),
    ("M862.1", "Cura", "['M862.1'] Check nozzle diameter (prusa only, undecoded): ['M862.1']"),
    ("M862.3", "", "['M862.3'] Model name (prusa only, undecoded): ['M862.3']"),
    ("M862.3", "Slic3r", "['M862.3'] Model name (prusa only, undecoded): ['M862.3']"),
    ("M862.3", "Cura", "['M862.3'] Model name (prusa only, undecoded): ['M862.3']"),
    ("M900", "", "['M900'] Set Linear Advance Scaling Factors"),
    ("M900", "Cura", "['M900'] Set Linear Advance Scaling Factors"),
    ("M907", "", "['M907'] Set digital trimpot motor current"),
    ("M907", "Slic3r", "['M907'] Set digital trimpot motor current"),
    ("M907", "Cura", "['M907'] Set digital trimpot motor current"),
]


@pytest.mark.parametrize("gcode,generator,expected_message", generator_specific_gcode_wrong_generator_testdata)
def test_decode_gcode_line_invalid_generator_specific_error_message(gcode, generator, expected_message):
    # arrange
    meta_infos = FileMetaInfos()
    meta_infos.generator = generator
    printer = PrinterModel()
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, gcode, printer)

    # assert
    assert(decoded) == "Unexpected generator " + generator + " for firmware dependent: " + expected_message


# We've checked all the invalid generator messages already above,
# only check here if an Exception is raised if stopOnUndecoded is True
def test_decode_gcode_line_invalid_generator_specific_raises_exception():
    # arrange
    meta_infos = FileMetaInfos()
    meta_infos.generator = "abc"
    printer = PrinterModel()
    decode_line = GDecoderLine()
    decode_line.stop_on_undecoded = True

    # act
    with pytest.raises(Exception) as e_info:
        decode_line.decode_gcode_line(meta_infos, "M203", printer)

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "Unexpected generator abc for firmware dependent: ['M203']"


valid_gcode_feedrate_testdata = [
    ("G0", "Rapid Move (no print)"),
    ("G1", "Linear Move (print)"),
    ("G2", "Clockwise Arc Move (print)"),
    ("G3", "Counter-Clockwise Arc Move (print)"),
]


@pytest.mark.parametrize("gcode,expected_decode_part", valid_gcode_feedrate_testdata)
def test_decode_gcode_line_valid_command_with_feedrate_expected_feedrate(gcode, expected_decode_part):
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, gcode + " F100", printer)

    # assert
    assert(decoded) == expected_decode_part + ", Feedrate: 100 mm/min"
    assert(printer.feedrate) == "100"


def test_decode_gcode_line_g0_x1_y2_z3_position_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "G0 X1 Y2 Z3", printer)

    # assert
    assert(decoded) == "Rapid Move (no print), X: 1 mm, Y: 2 mm, Z: 3 mm"
    assert(printer.position_x.get()) == "1"
    assert(printer.position_y.get()) == "2"
    assert(printer.position_z.get()) == "3"


def test_decode_gcode_line_g1_x1_y2_z3_e4_position_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "G1 X1 Y2 Z3 E4", printer)

    # assert
    assert(decoded) == "Linear Move (print), X: 1 mm, Y: 2 mm, Z: 3 mm, E: 4 mm"
    assert(printer.position_x.get()) == "1"
    assert(printer.position_y.get()) == "2"
    assert(printer.position_z.get()) == "3"
    assert(printer.extruder_physical.get()) == "4.0"


def test_decode_gcode_line_g2_x1_y2_i3_j4_e5_position_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "G2 X1 Y2 I3 J4 E5", printer)

    # assert
    assert(decoded) == "Clockwise Arc Move (print), X:1, Y:2, I (distant X): 3, J (distant Y): 4, E: 5 mm"
    assert(printer.position_x.get()) == "1"
    assert(printer.position_y.get()) == "2"
    assert(printer.extruder_physical.get()) == "5.0"


def test_decode_gcode_line_g3_x1_y2_i3_j4_e5_position_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "G3 X1 Y2 I3 J4 E5", printer)

    # assert
    assert(decoded) == "Counter-Clockwise Arc Move (print), X:1, Y:2, I (distant X): 3, J (distant Y): 4, E: 5 mm"
    assert(printer.position_x.get()) == "1"
    assert(printer.position_y.get()) == "2"
    assert(printer.extruder_physical.get()) == "5.0"


simple_gcode_testdata = [
    ("G4", "Dwell (aka: Pause)"),
    ("G21", "Set Units to Millimeters"),
    ("G28 F100 W",
        "Move to Origin (Home, often: X=0, Y=0; Z=0), "
        "unknown parameter (maybe feedrate?): F100, Suppress mesh bed leveling (Prusa only)"),
    ("G80", "Mesh-based Z probe"),
    ("G90", "Set to Absolute Positioning"),
    ("G91", "Set to Relative Positioning"),
    ("G92", "Set Position"),
    ("M73 P1 Q2 R3 S4",
        "Set/Get build percentage, "
        "Normal mode: 1 %, Silent mode: 2 %, Remaining in normal mode: 3 min., Remaining in silent mode: 4 min."),
    ("M84", "Stop idle hold (disable motors)"),
    ("M105", "Get Extruder Temperature"),
    ("M115 U1", "Get Firmware Version and Capabilities, Check the firmware version: 1"),
    ("M117 Message to be displayed", "Display Message: \"Message to be displayed\""),
    ("M190 S50", "Wait for bed temperature to reach target temp, Target: 50 °C"),
    ("M201 X1 Y2 Z3 E4", "Set max acceleration, X: 1 mm/s², Y: 2 mm/s², Z: 3 mm/s², E: 4 mm/s²"),
    ("M300 P1 S2", "Play beep sound, duration: 1 ms, frequency: 2 Hz"),
]


@pytest.mark.parametrize("gcode,expected_message", simple_gcode_testdata)
def test_decode_gcode_line_simple_command_message(gcode, expected_message):
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, gcode, printer)

    # assert
    assert(decoded) == expected_message


g28_xy_testdata = [
    ("", "Move to Origin (Home, often: X=0, Y=0; Z=0)", "0", "0"),
    ("X0", "Move to Origin (Home, often: X=0, Y=0; Z=0), X axis origin: 0", "0", "20"),
    ("Y0", "Move to Origin (Home, often: X=0, Y=0; Z=0), Y axis origin: 0", "10", "0"),
]


@pytest.mark.parametrize("xy,expected_message,expected_x,expected_y", g28_xy_testdata)
def test_decode_gcode_line_g28xy_position_xy(xy, expected_message, expected_x, expected_y):
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    printer._move_x("10")
    printer._move_y("20")
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "G28 " + xy, printer)

    # assert
    assert(decoded) == expected_message
    assert(printer.position_x.get()) == expected_x
    assert(printer.position_y.get()) == expected_y


def test_decode_gcode_line_g92_e10_extruder_position_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    printer.set_extruder_position("0")
    assert(printer.extruder_logical.get()) == "0"
    assert(printer.extruder_physical.get()) == "0"
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "G92 E10", printer)

    # assert
    assert(decoded) == "Set Position, new extruder position: 10 mm"
    assert(printer.extruder_logical.get()) == "10"
    assert(printer.extruder_physical.get()) == "0"


def test_decode_gcode_line_m104_s50_extruder_temp_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    assert(printer.extruder_temp.get()) == "?"
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "M104 S50", printer)

    # assert
    assert(decoded) == "Set Extruder Temperature, Target: 50 °C"
    assert(printer.extruder_temp.get()) == "50"


def test_decode_gcode_line_m106_s50_fan_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    assert(printer.fan.get()) == "?"
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "M106 S50", printer)

    # assert
    assert(decoded) == "Fan On, Fan Speed: 50 (0-255)"
    assert(printer.fan.get()) == "50"


def test_decode_gcode_line_m109_s50_extruder_temp_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    assert(printer.extruder_temp.get()) == "?"
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "M109 S50", printer)

    # assert
    assert(decoded) == "Set Extruder Temperature and Wait, Target: 50 °C"
    assert(printer.extruder_temp.get()) == "50"


def test_decode_gcode_line_m140_s50_bed_temp_ok():
    # arrange
    meta_infos = FileMetaInfos()
    printer = PrinterModel()
    assert(printer.bed_temp.get()) == "?"
    decode_line = GDecoderLine()

    # act
    decoded = decode_line.decode_gcode_line(meta_infos, "M140 S50", printer)

    # assert
    assert(decoded) == "Set Bed Temperature (Fast), Target: 50 °C"
    assert(printer.bed_temp.get()) == "50"
