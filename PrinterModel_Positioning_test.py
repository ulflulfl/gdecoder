from PrinterModel import *
import pytest


def test_Defaults():
  # arrange
  printer = PrinterModel()

  # assert
  assert(printer.positioningMode == "absolute")
  assert(printer.feedrate == "?")


def test_setPositioningMode_ValidInput_Ok():
  # arrange
  printer = PrinterModel()

  # act
  printer.setPositioningMode("absolute")

  # assert
  assert(printer.positioningMode == "absolute")

  # act
  printer.setPositioningMode("relative")

  # assert
  assert(printer.positioningMode == "relative")


def test_setPositioningMode_InvalidInput_RaisesException():
  # arrange
  printer = PrinterModel()

  # act
  with pytest.raises(Exception) as e_info:
      printer.setPositioningMode("invalid")

  # assert
  exception_msg = e_info.value.args[0]
  assert exception_msg == "setPositioningMode: Unexpected value: invalid"


def test_setFeedrate():
  # arrange
  printer = PrinterModel()

  # act
  printer.setFeedrate("100")

  # assert
  assert(printer.feedrate == "100")

def test_home_noXYZ_positionBecomes0():
  # arrange
  printer = PrinterModel()
  printer._moveX("1")
  printer._moveY("2")
  printer._moveZ("3")

  # act
  printer.home("", "")

  # assert
  assert(printer.positionX.get() == "0")
  assert(printer.positionY.get() == "0")
  assert(printer.positionZ.get() == "0")

def test_home_XY_UnchangedZ():
  # arrange
  printer = PrinterModel()
  printer._moveX("1")
  printer._moveY("2")
  printer._moveZ("3")

  # act
  printer.home("0", "0")

  # assert
  assert(printer.positionX.get() == "0")
  assert(printer.positionY.get() == "0")
  assert(printer.positionZ.get() == "3")

def test_home_Xnot0_Exception():
  # arrange
  printer = PrinterModel()

  # act / assert
  with pytest.raises(Exception) as e_info:
    printer.home("1", "0")

def test_home_Ynot0_Exception():
  # arrange
  printer = PrinterModel()

  # act / assert
  with pytest.raises(Exception) as e_info:
    printer.home("0", "1")


def test_move_allDirectionsSet_positionOk():
  # arrange
  printer = PrinterModel()

  # act
  printer.move("1", "2", "3")

  # assert
  assert(printer.positionX.get() == "1")
  assert(printer.positionY.get() == "2")
  assert(printer.positionZ.get() == "3")


def test_move_XinRelativeMode_raisesException():
  # arrange
  printer = PrinterModel()
  printer.setPositioningMode("relative")

  # act
  with pytest.raises(Exception) as e_info:
    printer.move("1", "", "")

  # assert
  exception_msg = e_info.value.args[0]
  assert exception_msg == "moveX: Positioning mode unexpected: relative"


def test_move_YinRelativeMode_raisesException():
  # arrange
  printer = PrinterModel()
  printer.setPositioningMode("relative")

  # act
  with pytest.raises(Exception) as e_info:
    printer.move("", "1", "")

  # assert
  exception_msg = e_info.value.args[0]
  assert exception_msg == "moveY: Positioning mode unexpected: relative"


def test_move_ZinRelativeModeWithoutInitialZ_raisesException():
  # arrange
  printer = PrinterModel()
  printer.setPositioningMode("relative")

  # act
  with pytest.raises(Exception) as e_info:
    printer.move("", "", "1")

  # assert
  exception_msg = e_info.value.args[0]
  assert exception_msg == "moveZ: relative Z move without initial positioning"


def test_move_ZinRelativeModeWithInitialZ_ZpositionOk():
  # arrange
  printer = PrinterModel()
  printer.home("", "")
  printer.setPositioningMode("relative")

  # act
  printer.move("", "", "1")

  # assert
  assert(printer.positionZ.get() == "1.0")

def test_move_ZinInvalidPositionMode_raisesException():
  # arrange
  printer = PrinterModel()
  printer.home("", "")
  printer.positioningMode = "invalid"

  # act
  with pytest.raises(Exception) as e_info:
    printer.move("", "", "1")

  # assert
  exception_msg = e_info.value.args[0]
  assert exception_msg == "moveZ: Positioning mode unexpected: invalid"
