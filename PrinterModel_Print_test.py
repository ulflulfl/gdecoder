from PrinterModel import PrinterModel
import pytest


def test_printX_AbsoluteMode_XPositionsOk():
    # arrange
    printer = PrinterModel()
    printer.setPositioningMode("absolute")
    printer.home("", "")
    printer._moveX("1")

    # act
    printer._printX("2")

    # assert
    assert(printer.positionX.get()) == "2"
    assert(printer.positionX.getMin()) == "0"
    assert(printer.positionX.getMax()) == "2"
    assert(printer.printPositionX.get()) == "2"
    assert(printer.printPositionX.getMin()) == "1"
    assert(printer.printPositionX.getMax()) == "2"


def test_printX_AbsoluteMode_printZUpdated():
    # arrange
    printer = PrinterModel()
    printer.setPositioningMode("absolute")
    printer.home("", "")
    printer._moveZ("1")
    assert(printer.printPositionZ.get()) == "?"

    # act
    printer._printX("2")

    # assert
    assert(printer.printPositionZ.get()) == "1"


def test_printX_RelativeMode_RaisesExeption():
    # arrange
    printer = PrinterModel()
    printer.setPositioningMode("relative")
    printer.home("", "")

    # act
    with pytest.raises(Exception) as e_info:
        printer._printX("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "relative X positions not implemented"


def test_printY_AbsoluteMode_YPositionsOk():
    # arrange
    printer = PrinterModel()
    printer.setPositioningMode("absolute")
    printer.home("", "")
    printer._moveY("1")

    # act
    printer._printY("2")

    # assert
    assert(printer.positionY.get()) == "2"
    assert(printer.positionY.getMin()) == "0"
    assert(printer.positionY.getMax()) == "2"
    assert(printer.printPositionY.get()) == "2"
    assert(printer.printPositionY.getMin()) == "1"
    assert(printer.printPositionY.getMax()) == "2"


def test_printY_AbsoluteMode_printZUpdated():
    # arrange
    printer = PrinterModel()
    printer.setPositioningMode("absolute")
    printer.home("", "")
    printer._moveZ("1")
    assert(printer.printPositionZ.get()) == "?"

    # act
    printer._printY("2")

    # assert
    assert(printer.printPositionZ.get()) == "1"


def test_printY_RelativeMode_RaisesExeption():
    # arrange
    printer = PrinterModel()
    printer.setPositioningMode("relative")
    printer.home("", "")

    # act
    with pytest.raises(Exception) as e_info:
        printer._printY("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "relative Y positions not implemented"


def test_printZPhysical_PositionsOk():
    # arrange
    printer = PrinterModel()
    printer.home("", "")
    printer._moveZ("1")

    # act
    printer._printZPhysical("2")

    # assert
    assert(printer.positionZ.get()) == "2"
    assert(printer.positionZ.getMin()) == "0"
    assert(printer.positionZ.getMax()) == "2"
    assert(printer.printPositionZ.get()) == "2"
    assert(printer.printPositionZ.getMin()) == "1"
    assert(printer.printPositionZ.getMax()) == "2"


def test_printZ_Absolute_PositionsOk():
    # arrange
    printer = PrinterModel()
    printer.home("", "")
    printer._moveZ("1")

    # act
    printer._printZ("2")

    # assert
    assert(printer.positionZ.get()) == "2"
    assert(printer.positionZ.getMin()) == "0"
    assert(printer.positionZ.getMax()) == "2"
    assert(printer.printPositionZ.get()) == "2"
    assert(printer.printPositionZ.getMin()) == "1"
    assert(printer.printPositionZ.getMax()) == "2"


def test_printZ_Relative_PositionsOk():
    # arrange
    printer = PrinterModel()
    printer.home("", "")
    printer._moveZ("1")
    printer.setPositioningMode("relative")

    # act
    printer._printZ("2")

    # assert
    assert(printer.positionZ.get()) == "3.0"
    assert(printer.positionZ.getMin()) == "0"
    assert(printer.positionZ.getMax()) == "3.0"
    assert(printer.printPositionZ.get()) == "3.0"
    assert(printer.printPositionZ.getMin()) == "1"
    assert(printer.printPositionZ.getMax()) == "3.0"


def test_printZ_NoInitialPositionInRelative_RaisesException():
    # arrange
    printer = PrinterModel()
    printer.setPositioningMode("relative")

    # act
    with pytest.raises(Exception) as e_info:
        printer._printZ("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "printZ: relative Z move without initial positioning"


def test_printZ_InvalidPositioningMode_RaisesException():
    # arrange
    printer = PrinterModel()
    printer.positioningMode = "invalid"

    # act
    with pytest.raises(Exception) as e_info:
        printer._printZ("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "printZ: Positioning mode unexpected: invalid"


def test_printLinear():
    # arrange
    printer = PrinterModel()
    printer.home("", "")

    # act
    printer.printLinear("1", "2", "3", "4")

    # assert
    assert(printer.positionX.get()) == "1"
    assert(printer.positionY.get()) == "2"
    assert(printer.positionZ.get()) == "3"
    assert(printer.extruderPhysical.get()) == "4.0"


def test_printCW():
    # arrange
    printer = PrinterModel()
    printer.home("", "")

    # act
    printer.printCW("1", "2", "3", "4", "5")

    # assert
    assert(printer.positionX.get()) == "1"
    assert(printer.positionY.get()) == "2"
    assert(printer.extruderPhysical.get()) == "5.0"


def test_printCCW():
    # arrange
    printer = PrinterModel()
    printer.home("", "")

    # act
    printer.printCCW("1", "2", "3", "4", "5")

    # assert
    assert(printer.positionX.get()) == "1"
    assert(printer.positionY.get()) == "2"
    assert(printer.extruderPhysical.get()) == "5.0"
