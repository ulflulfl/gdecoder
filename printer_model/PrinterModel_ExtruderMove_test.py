from PrinterModel import PrinterModel
import pytest
pytestmark = pytest.mark.unittests


def test_defaults():
    # arrange
    printer = PrinterModel()

    # assert
    assert(printer.extruder_move_mode == "absolute")
    assert(printer.extruder_physical.get()) == "0"
    assert(printer.extruder_physical.get_max()) == "0"
    assert(printer.extruder_logical.get()) == "0"


def test_set_extruder_move_mode_invalid_move_mode_raises_exception():
    # arrange
    printer = PrinterModel()

    # act
    with pytest.raises(Exception) as e_info:
        printer.set_extruder_move_mode("invalid")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "setExtruderMoveMode: Unexpected value: invalid"


def test_print_e_absolute():
    # arrange
    printer = PrinterModel()
    printer.set_extruder_move_mode("absolute")

    # act
    printer._print_e("10")

    # assert
    assert(printer.extruder_physical.get()) == "10.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "10.0"


def test_print_e_absolute_retract():
    # arrange
    printer = PrinterModel()
    printer.set_extruder_move_mode("absolute")
    printer._print_e("10")
    assert(printer.extruder_physical.get()) == "10.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "10.0"

    # act
    printer._print_e("-5")

    # assert
    assert(printer.extruder_physical.get()) == "-5.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "-5.0"


def test_print_e_relative():
    # arrange
    printer = PrinterModel()
    printer.set_extruder_move_mode("relative")
    assert(printer.extruder_physical.get()) == "0"
    assert(printer.extruder_physical.get_max()) == "0"
    assert(printer.extruder_logical.get()) == "0"

    # act
    printer._print_e("10")

    # assert
    assert(printer.extruder_physical.get()) == "10.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "10.0"


def test_print_e_relative_retract():
    # arrange
    printer = PrinterModel()
    printer.set_extruder_move_mode("relative")
    printer._print_e("10")
    assert(printer.extruder_physical.get()) == "10.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "10.0"

    # act
    printer._print_e("-1")

    # assert
    assert(printer.extruder_physical.get()) == "9.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "9.0"


def test_set_extruder_position():
    # arrange
    printer = PrinterModel()
    printer.set_extruder_move_mode("relative")
    printer._print_e("10")
    assert(printer.extruder_physical.get()) == "10.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "10.0"

    # act
    printer.set_extruder_position("1.0")

    # assert
    assert(printer.extruder_physical.get()) == "10.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "1.0"


def test_print_e_given_position_new_position_ok():
    # arrange
    printer = PrinterModel()
    printer.set_extruder_move_mode("relative")
    printer._print_e("10")
    printer.set_extruder_position("0.0")
    assert(printer.extruder_physical.get()) == "10.0"
    assert(printer.extruder_physical.get_max()) == "10.0"
    assert(printer.extruder_logical.get()) == "0.0"

    # act
    printer._print_e("1")

    # assert
    assert(printer.extruder_physical.get()) == "11.0"
    assert(printer.extruder_physical.get_max()) == "11.0"
    assert(printer.extruder_logical.get()) == "1.0"


def test_print_e_invalid_move_mode_raises_exception():
    # arrange
    printer = PrinterModel()
    printer.extruder_move_mode = "invalid"

    # act / assert
    with pytest.raises(Exception) as e_info:
        printer._print_e("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "extruder move mode not implemented: invalid"
