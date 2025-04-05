from PrinterModel import PrinterModel
import pytest
pytestmark = pytest.mark.unittests


def test_defaults():
    # arrange
    printer = PrinterModel()

    # assert
    assert(printer.positioning_mode == "absolute")
    assert(printer.feedrate == "?")


def test_set_positioning_mode_valid_input_ok():
    # arrange
    printer = PrinterModel()

    # act
    printer.set_positioning_mode("absolute")

    # assert
    assert(printer.positioning_mode == "absolute")

    # act
    printer.set_positioning_mode("relative")

    # assert
    assert(printer.positioning_mode == "relative")


def test_set_positioning_mode_invalid_input_raises_exception():
    # arrange
    printer = PrinterModel()

    # act
    with pytest.raises(Exception) as e_info:
        printer.set_positioning_mode("invalid")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "setPositioningMode: Unexpected value: invalid"


def test_set_feedrate():
    # arrange
    printer = PrinterModel()

    # act
    printer.set_feedrate("100")

    # assert
    assert(printer.feedrate == "100")


def test_home_no_xyz_position_becomes_0():
    # arrange
    printer = PrinterModel()
    printer._move_x("1")
    printer._move_y("2")
    printer._move_z("3")

    # act
    printer.home("", "")

    # assert
    assert(printer.position_x.get() == "0")
    assert(printer.position_y.get() == "0")
    assert(printer.position_z.get() == "0")


def test_home_xy_unchanged_z():
    # arrange
    printer = PrinterModel()
    printer._move_x("1")
    printer._move_y("2")
    printer._move_z("3")

    # act
    printer.home("0", "0")

    # assert
    assert(printer.position_x.get() == "0")
    assert(printer.position_y.get() == "0")
    assert(printer.position_z.get() == "3")


def test_home_xnot0_raises_exception():
    # arrange
    printer = PrinterModel()

    # act / assert
    with pytest.raises(Exception) as e_info:
        printer.home("1", "0")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "homeX: Unexpected value: 1"


def test_home_ynot0_raises_exception():
    # arrange
    printer = PrinterModel()

    # act / assert
    with pytest.raises(Exception) as e_info:
        printer.home("0", "1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "homeY: Unexpected value: 1"


def test_move_all_directions_set_position_ok():
    # arrange
    printer = PrinterModel()

    # act
    printer.move("1", "2", "3")

    # assert
    assert(printer.position_x.get() == "1")
    assert(printer.position_y.get() == "2")
    assert(printer.position_z.get() == "3")


def test_move_x_in_relative_mode_raises_exception():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("relative")

    # act
    with pytest.raises(Exception) as e_info:
        printer.move("1", "", "")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "moveX: Positioning mode unexpected: relative"


def test_move_y_in_relative_mode_raises_exception():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("relative")

    # act
    with pytest.raises(Exception) as e_info:
        printer.move("", "1", "")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "moveY: Positioning mode unexpected: relative"


def test_move_z_in_relative_mode_without_initial_z_raises_exception():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("relative")

    # act
    with pytest.raises(Exception) as e_info:
        printer.move("", "", "1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "moveZ: relative Z move without initial positioning"


def test_move_z_in_relative_mode_with_initial_z_z_position_ok():
    # arrange
    printer = PrinterModel()
    printer.home("", "")
    printer.set_positioning_mode("relative")

    # act
    printer.move("", "", "1")

    # assert
    assert(printer.position_z.get() == "1.0")


def test_move_z_in_invalid_position_mode_raises_exception():
    # arrange
    printer = PrinterModel()
    printer.home("", "")
    printer.positioning_mode = "invalid"

    # act
    with pytest.raises(Exception) as e_info:
        printer.move("", "", "1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "moveZ: Positioning mode unexpected: invalid"
