from PrinterModel import PrinterModel
import pytest
pytestmark = pytest.mark.unittests


def test_setBedTemperature():
    # arrange
    printer = PrinterModel()
    assert(printer.bedTemp.get()) == "?"

    # act
    printer.setBedTemperature("100")

    # assert
    assert(printer.bedTemp.get()) == "100"


def test_setExtruderTemperature():
    # arrange
    printer = PrinterModel()
    assert(printer.extruderTemp.get()) == "?"

    # act
    printer.setExtruderTemperature("100")

    # assert
    assert(printer.extruderTemp.get()) == "100"


def test_setFan():
    # arrange
    printer = PrinterModel()
    assert(printer.fan.get()) == "?"

    # act
    printer.setFan("100")

    # assert
    assert(printer.fan.get()) == "100"
