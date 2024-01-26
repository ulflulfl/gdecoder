import pytest
from GDecoderLine import GDecoderLine
from PrinterModel import PrinterModel
from FileMetaInfos import FileMetaInfos


def test_decodeGCodeLine_empty_empty():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "", printer)

    # assert
    assert(decoded) == ""


invalid_gcode_testdata = [
    ("invalid", "", "Unknown gcode: invalid"),
    ("G0 invalidCommand",
        "Rapid Move, ", "Unknown subtoken: invalidCommand in: ['G0', 'invalidCommand']"),
    ("G1 invalidCommand", "Linear Move, ", "Unknown subtoken: invalidCommand in: ['G1', 'invalidCommand']"),
    ("G2 invalidCommand", "Clockwise Arc Move, ", "Unknown subtoken: invalidCommand in: ['G2', 'invalidCommand']"),
    ("G3 invalidCommand", "Counter-Clockwise Arc Move, ", "Unknown subtoken: invalidCommand in: ['G3', 'invalidCommand']"),
    ("G4 invalidCommand", "Dwell (aka: Pause), ", "Unknown subtoken: invalidCommand in: ['G4', 'invalidCommand']"),
    ("G21 invalidCommand", "Set Units to Millimeters, ", "Unknown subtoken: invalidCommand in: ['G21', 'invalidCommand']"),
    ("G28 invalidCommand",
        "Move to Origin (Home, often: X=0, Y=0; Z=0), ", "Unknown subtoken: invalidCommand in: ['G28', 'invalidCommand']"),
    ("G80 invalidCommand", "Mesh-based Z probe, ", "Unknown subtoken: invalidCommand in: ['G80', 'invalidCommand']"),
    ("G90 invalidCommand", "Set to Absolute Positioning, ", "Unknown subtoken: invalidCommand in: ['G90', 'invalidCommand']"),
    ("G91 invalidCommand", "Set to Relative Positioning, ", "Unknown subtoken: invalidCommand in: ['G91', 'invalidCommand']"),
    ("G92 invalidCommand", "Set Position, ", "Unknown subtoken: invalidCommand in: ['G92', 'invalidCommand']"),
    ("M73 invalidCommand", "Set/Get build percentage, ", "Unknown subtoken: invalidCommand in: ['M73', 'invalidCommand']"),
    ("M82 invalidCommand",
        "Set extruder to absolute mode, ", "Unknown subtoken: invalidCommand in: ['M82', 'invalidCommand']"),
    ("M83 invalidCommand",
        "Set extruder to relative mode, ", "Unknown subtoken: invalidCommand in: ['M83', 'invalidCommand']"),
    ("M84 invalidCommand", "Stop idle hold, ", "Unknown subtoken: invalidCommand in: ['M84', 'invalidCommand']"),
    ("M104 invalidCommand", "Set Extruder Temperature, ", "Unknown subtoken: invalidCommand in: ['M104', 'invalidCommand']"),
    ("M105 invalidCommand", "Get Extruder Temperature, ", "Unknown subtoken: invalidCommand in: ['M105', 'invalidCommand']"),
    ("M106 invalidCommand", "Fan On, ", "Unknown subtoken: invalidCommand in: ['M106', 'invalidCommand']"),
    ("M107 invalidCommand", "Fan Off, ", "Unknown subtoken: invalidCommand in: ['M107', 'invalidCommand']"),
    ("M109 invalidCommand",
        "Set Extruder Temperature and Wait, ", "Unknown subtoken: invalidCommand in: ['M109', 'invalidCommand']"),
    ("M115 invalidCommand",
        "Get Firmware Version and Capabilities, ", "Unknown subtoken: invalidCommand in: ['M115', 'invalidCommand']"),
    # ("M117 invalidCommand", "", "Display Message: invalidCommand"),
    ("M140 invalidCommand", "Set Bed Temperature (Fast), ", "Unknown subtoken: invalidCommand in: ['M140', 'invalidCommand']"),
    ("M190 invalidCommand",
        "Wait for bed temperature to reach target temp, ", "Unknown subtoken: invalidCommand in: ['M190', 'invalidCommand']"),
    ("M201 invalidCommand", "Set max acceleration, ", "Unknown subtoken: invalidCommand in: ['M201', 'invalidCommand']"),
    # ("M203 invalidCommand", "Set maximum feedrate, ", "Unknown subtoken: invalidCommand in: ['M203', 'invalidCommand']"),
    # ("M204 invalidCommand", "", ""),
    # ("M205 invalidCommand", "", ""),
    # ("M221 invalidCommand", "", ""),
    ("M300 invalidCommand", "Play beep sound, ", "Unknown subtoken: invalidCommand in: ['M300', 'invalidCommand']"),
    # ("M862.1 invalidCommand", "", ""),
    # ("M862.3 invalidCommand", "", ""),
    # ("M900 invalidCommand", "", ""),
    # ("M907 invalidCommand", "", ""),
]


@pytest.mark.parametrize("gcode,expected_decode,expected_message", invalid_gcode_testdata)
def test_decodeGCodeLine_InvalidCommand_ErrorMessage(gcode, expected_decode, expected_message):
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, gcode, printer)

    # assert
    assert(decoded) == expected_decode + expected_message


@pytest.mark.parametrize("gcode,expected_decode,expected_message", invalid_gcode_testdata)
def test_decodeGCodeLine_invalidCommand_raisesException(gcode, expected_decode, expected_message):
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()
    decodeLine.stopOnUndecoded = True

    # act
    with pytest.raises(Exception) as e_info:
        decodeLine.decodeGCodeLine(metaInfos, gcode, printer)

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == expected_message


valid_gcode_feedrate_testdata = [
    ("G0", "Rapid Move"),
    ("G1", "Linear Move"),
    ("G2", "Clockwise Arc Move"),
    ("G3", "Counter-Clockwise Arc Move"),
]


@pytest.mark.parametrize("gcode,expected_decode_part", valid_gcode_feedrate_testdata)
def test_decodeGCodeLine_validCommandWithFeedrate_raisesException(gcode, expected_decode_part):
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, gcode + " F100", printer)

    # assert
    assert(decoded) == expected_decode_part + ", Feedrate: 100 mm/min"
    assert(printer.feedrate) == "100"


def test_decodeGCodeLine_G0X1Y2Z3_positionOk():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G0 X1 Y2 Z3", printer)

    # assert
    assert(decoded) == "Rapid Move, X: 1 mm, Y: 2 mm, Z: 3 mm"
    assert(printer.positionX.get()) == "1"
    assert(printer.positionY.get()) == "2"
    assert(printer.positionZ.get()) == "3"


def test_decodeGCodeLine_G1X1Y2Z3E4_positionOk():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G1 X1 Y2 Z3 E4", printer)

    # assert
    assert(decoded) == "Linear Move, X: 1 mm, Y: 2 mm, Z: 3 mm, E: 4 mm"
    assert(printer.positionX.get()) == "1"
    assert(printer.positionY.get()) == "2"
    assert(printer.positionZ.get()) == "3"
    assert(printer.extruderPhysical.get()) == "4.0"


def test_decodeGCodeLine_G2X1Y2I3J4E5_positionOk():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G2 X1 Y2 I3 J4 E5", printer)

    # assert
    assert(decoded) == "Clockwise Arc Move, X:1, Y:2, I (distant X): 3, J (distant Y): 4, E: 5 mm"
    assert(printer.positionX.get()) == "1"
    assert(printer.positionY.get()) == "2"
    assert(printer.extruderPhysical.get()) == "5.0"


def test_decodeGCodeLine_G3X1Y2I3J4E5_positionOk():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    printer.home("", "")
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G3 X1 Y2 I3 J4 E5", printer)

    # assert
    assert(decoded) == "Counter-Clockwise Arc Move, X:1, Y:2, I (distant X): 3, J (distant Y): 4, E: 5 mm"
    assert(printer.positionX.get()) == "1"
    assert(printer.positionY.get()) == "2"
    assert(printer.extruderPhysical.get()) == "5.0"


def test_decodeGCodeLine_G4_Message():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G4", printer)

    # assert
    assert(decoded) == "Dwell (aka: Pause)"


def test_decodeGCodeLine_G21_Message():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G21", printer)

    # assert
    assert(decoded) == "Set Units to Millimeters"
