from PrinterModel import PrinterModel
import pytest
pytestmark = pytest.mark.unittests


def test_set_bed_temperature():
    # arrange
    printer = PrinterModel()
    assert(printer.bed_temp.get()) == "?"

    # act
    printer.set_bed_temperature("100")

    # assert
    assert(printer.bed_temp.get()) == "100"


def test_set_extruder_temperature():
    # arrange
    printer = PrinterModel()
    assert(printer.extruder_temp.get()) == "?"

    # act
    printer.set_extruder_temperature("100")

    # assert
    assert(printer.extruder_temp.get()) == "100"


def test_set_fan():
    # arrange
    printer = PrinterModel()
    assert(printer.fan.get()) == "?"

    # act
    printer.set_fan("100")

    # assert
    assert(printer.fan.get()) == "100"
