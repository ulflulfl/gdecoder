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


def test_decodeGCodeLine_invalid_errorMessage():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "invalid", printer)

    # assert
    assert(decoded) == "Unknown gcode: invalid"


def test_decodeGCodeLine_invalidWithStopFlag_raisesException():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()
    decodeLine.stopOnUndecoded = True

    # act
    with pytest.raises(Exception) as e_info:
        decodeLine.decodeGCodeLine(metaInfos, "invalid", printer)

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "Unknown gcode: invalid"


def test_decodeGCodeLine_G0F100_feedrate100():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G0 F100", printer)

    # assert
    assert(decoded) == "Rapid Move, Feedrate: 100 mm/min."
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


def test_decodeGCodeLine_G0Invalid_errorMessage():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G0 Invalid", printer)

    # assert
    assert(decoded) == "Rapid Move, Unknown subtoken: Invalid in: ['G0', 'Invalid']"


def test_decodeGCodeLine_G0InvalidWithStopFlag_raisesException():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()
    decodeLine.stopOnUndecoded = True

    # act
    with pytest.raises(Exception) as e_info:
        decodeLine.decodeGCodeLine(metaInfos, "G0 invalid", printer)

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "Unknown subtoken: invalid in: ['G0', 'invalid']"


def test_decodeGCodeLine_G1F100_feedrate100():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G1 F100", printer)

    # assert
    assert(decoded) == "Linear Move, Feedrate: 100 mm/min."
    assert(printer.feedrate) == "100"


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


def test_decodeGCodeLine_G1Invalid_errorMessage():
    # arrange
    metaInfos = FileMetaInfos()
    printer = PrinterModel()
    decodeLine = GDecoderLine()

    # act
    decoded = decodeLine.decodeGCodeLine(metaInfos, "G1 Invalid", printer)

    # assert
    assert(decoded) == "Linear Move, Unknown subtoken: Invalid in: ['G1', 'Invalid']"
