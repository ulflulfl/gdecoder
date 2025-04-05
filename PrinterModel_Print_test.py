from PrinterModel import PrinterModel
import pytest
pytestmark = pytest.mark.unittests


def test_printx_absolute_mode_x_positions_ok():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("absolute")
    printer.home("", "")
    printer._move_x("1")

    # act
    printer._print_x("2")

    # assert
    assert(printer.position_x.get()) == "2"
    assert(printer.position_x.get_min()) == "0"
    assert(printer.position_x.get_max()) == "2"
    assert(printer.print_position_x.get()) == "2"
    assert(printer.print_position_x.get_min()) == "1"
    assert(printer.print_position_x.get_max()) == "2"


def test_printx_absolute_mode_printz_updated():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("absolute")
    printer.home("", "")
    printer._move_z("1")
    assert(printer.print_position_z.get()) == "?"

    # act
    printer._print_x("2")

    # assert
    assert(printer.print_position_z.get()) == "1"


def test_printx_relative_mode_raises_exeption():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("relative")
    printer.home("", "")

    # act
    with pytest.raises(Exception) as e_info:
        printer._print_x("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "relative X positions not implemented"


def test_printy_absolute_mode_y_positions_ok():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("absolute")
    printer.home("", "")
    printer._move_y("1")

    # act
    printer._print_y("2")

    # assert
    assert(printer.position_y.get()) == "2"
    assert(printer.position_y.get_min()) == "0"
    assert(printer.position_y.get_max()) == "2"
    assert(printer.print_position_y.get()) == "2"
    assert(printer.print_position_y.get_min()) == "1"
    assert(printer.print_position_y.get_max()) == "2"


def test_printy_absolute_mode_printz_updated():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("absolute")
    printer.home("", "")
    printer._move_z("1")
    assert(printer.print_position_z.get()) == "?"

    # act
    printer._print_y("2")

    # assert
    assert(printer.print_position_z.get()) == "1"


def test_printy_relative_mode_raises_exeption():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("relative")
    printer.home("", "")

    # act
    with pytest.raises(Exception) as e_info:
        printer._print_y("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "relative Y positions not implemented"


def test_printz_physical_positions_ok():
    # arrange
    printer = PrinterModel()
    printer.home("", "")
    printer._move_z("1")

    # act
    printer._print_z_physical("2")

    # assert
    assert(printer.position_z.get()) == "2"
    assert(printer.position_z.get_min()) == "0"
    assert(printer.position_z.get_max()) == "2"
    assert(printer.print_position_z.get()) == "2"
    assert(printer.print_position_z.get_min()) == "1"
    assert(printer.print_position_z.get_max()) == "2"


def test_printz_absolute_positions_ok():
    # arrange
    printer = PrinterModel()
    printer.home("", "")
    printer._move_z("1")

    # act
    printer._print_z("2")

    # assert
    assert(printer.position_z.get()) == "2"
    assert(printer.position_z.get_min()) == "0"
    assert(printer.position_z.get_max()) == "2"
    assert(printer.print_position_z.get()) == "2"
    assert(printer.print_position_z.get_min()) == "1"
    assert(printer.print_position_z.get_max()) == "2"


def test_printz_relative_positions_ok():
    # arrange
    printer = PrinterModel()
    printer.home("", "")
    printer._move_z("1")
    printer.set_positioning_mode("relative")

    # act
    printer._print_z("2")

    # assert
    assert(printer.position_z.get()) == "3.0"
    assert(printer.position_z.get_min()) == "0"
    assert(printer.position_z.get_max()) == "3.0"
    assert(printer.print_position_z.get()) == "3.0"
    assert(printer.print_position_z.get_min()) == "1"
    assert(printer.print_position_z.get_max()) == "3.0"


def test_printz_no_initial_position_in_relative_raises_exception():
    # arrange
    printer = PrinterModel()
    printer.set_positioning_mode("relative")

    # act
    with pytest.raises(Exception) as e_info:
        printer._print_z("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "printZ: relative Z move without initial positioning"


def test_printz_invalid_positioning_mode_raises_exception():
    # arrange
    printer = PrinterModel()
    printer.positioning_mode = "invalid"

    # act
    with pytest.raises(Exception) as e_info:
        printer._print_z("1")

    # assert
    exception_msg = e_info.value.args[0]
    assert exception_msg == "printZ: Positioning mode unexpected: invalid"


def test_print_linear():
    # arrange
    printer = PrinterModel()
    printer.home("", "")

    # act
    printer.print_linear("1", "2", "3", "4")

    # assert
    assert(printer.position_x.get()) == "1"
    assert(printer.position_y.get()) == "2"
    assert(printer.position_z.get()) == "3"
    assert(printer.extruder_physical.get()) == "4.0"


def test_print_cw():
    # arrange
    printer = PrinterModel()
    printer.home("", "")

    # act
    printer.print_cw("1", "2", "3", "4", "5")

    # assert
    assert(printer.position_x.get()) == "1"
    assert(printer.position_y.get()) == "2"
    assert(printer.extruder_physical.get()) == "5.0"


def test_print_ccw():
    # arrange
    printer = PrinterModel()
    printer.home("", "")

    # act
    printer.print_ccw("1", "2", "3", "4", "5")

    # assert
    assert(printer.position_x.get()) == "1"
    assert(printer.position_y.get()) == "2"
    assert(printer.extruder_physical.get()) == "5.0"
