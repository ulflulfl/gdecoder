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
    ("G0 invalidCommand", "Rapid Move, ", "Unknown subtoken: invalidCommand in: ['G0', 'invalidCommand']"),
    ("G1 invalidCommand", "Linear Move, ", "Unknown subtoken: invalidCommand in: ['G1', 'invalidCommand']"),
    ("G2 invalidCommand", "Clockwise Arc Move, ", "Unknown subtoken: invalidCommand in: ['G2', 'invalidCommand']"),
    ("G3 invalidCommand", "Counter-Clockwise Arc Move, ", "Unknown subtoken: invalidCommand in: ['G3', 'invalidCommand']"),
    ("G4 invalidCommand", "Dwell (aka: Pause), ", "Unknown subtoken: invalidCommand in: ['G4', 'invalidCommand']"),
    ("G21 invalidCommand", "Set Units to Millimeters, ", "Unknown subtoken: invalidCommand in: ['G21', 'invalidCommand']"),
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
