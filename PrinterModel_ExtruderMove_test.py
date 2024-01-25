from PrinterModel import *
import pytest


def test_Defaults():
  # arrange
  printer = PrinterModel()

  # assert
  assert(printer.extruderMoveMode == "absolute")
  assert(printer.extruderPhysical.get()) == "0"
  assert(printer.extruderPhysical.getMax()) == "0"
  assert(printer.extruderLogical.get()) == "0"


def test_setExtruderMoveMode_InvalidMoveMode_RaisesException():
  # arrange
  printer = PrinterModel()

  # act
  with pytest.raises(Exception) as e_info:
    printer.setExtruderMoveMode("invalid")

  # assert
  exception_msg = e_info.value.args[0]
  assert exception_msg == "setExtruderMoveMode: Unexpected value: invalid"


def test_printE_Absolute():
  # arrange
  printer = PrinterModel()
  printer.setExtruderMoveMode("absolute")

  # act
  printer._printE("10")

  # assert
  assert(printer.extruderPhysical.get()) == "10.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "10.0"


def test_printE_AbsoluteRetract():
  # arrange
  printer = PrinterModel()
  printer.setExtruderMoveMode("absolute")
  printer._printE("10")
  assert(printer.extruderPhysical.get()) == "10.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "10.0"

  # act
  printer._printE("-5")

  # assert
  assert(printer.extruderPhysical.get()) == "-5.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "-5.0"


def test_printE_Relative():
  # arrange
  printer = PrinterModel()
  printer.setExtruderMoveMode("relative")
  assert(printer.extruderPhysical.get()) == "0"
  assert(printer.extruderPhysical.getMax()) == "0"
  assert(printer.extruderLogical.get()) == "0"

  # act
  printer._printE("10")

  # assert
  assert(printer.extruderPhysical.get()) == "10.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "10.0"


def test_printE_RelativeRetract():
  # arrange
  printer = PrinterModel()
  printer.setExtruderMoveMode("relative")
  printer._printE("10")
  assert(printer.extruderPhysical.get()) == "10.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "10.0"

  # act
  printer._printE("-1")

  # assert
  assert(printer.extruderPhysical.get()) == "9.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "9.0"


def test_setExtruderPosition():
  # arrange
  printer = PrinterModel()
  printer.setExtruderMoveMode("relative")
  printer._printE("10")
  assert(printer.extruderPhysical.get()) == "10.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "10.0"

  # act
  printer.setExtruderPosition("1.0")

  # assert
  assert(printer.extruderPhysical.get()) == "10.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "1.0"


def test_printE_GivenPosition_NewPositionOk():
  # arrange
  printer = PrinterModel()
  printer.setExtruderMoveMode("relative")
  printer._printE("10")
  printer.setExtruderPosition("0.0")
  assert(printer.extruderPhysical.get()) == "10.0"
  assert(printer.extruderPhysical.getMax()) == "10.0"
  assert(printer.extruderLogical.get()) == "0.0"

  # act
  printer._printE("1")

  # assert
  assert(printer.extruderPhysical.get()) == "11.0"
  assert(printer.extruderPhysical.getMax()) == "11.0"
  assert(printer.extruderLogical.get()) == "1.0"


def test_printE_InvalidMoveMode_RaisesException():
  # arrange
  printer = PrinterModel()
  printer.extruderMoveMode = "invalid"

  # act / assert
  with pytest.raises(Exception) as e_info:
    printer._printE("1")

  # assert
  exception_msg = e_info.value.args[0]
  assert exception_msg == "extruder move mode not implemented: invalid"
