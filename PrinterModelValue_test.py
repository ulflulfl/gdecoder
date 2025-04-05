from PrinterModelValue import PrinterModelValue
import pytest
pytestmark = pytest.mark.unittests


def test_get_initial_question_mark():
    # arrange
    printer_value = PrinterModelValue()

    # act
    value = printer_value.get()

    # assert
    assert(value) == "?"


def test_set_value_ok():
    # arrange
    printer_value = PrinterModelValue()
    assert(printer_value.get()) == "?"

    # act / assert
    printer_value.set("100")
    assert(printer_value.get()) == "100"


def test_set_max_initial_ok():
    # arrange
    printer_value = PrinterModelValue()
    assert(printer_value.get_max()) == "?"

    # act
    printer_value.set("100")

    # assert
    assert(printer_value.get_max()) == "100"


def test_set_max_second_time_ok():
    # arrange
    printer_value = PrinterModelValue()
    printer_value.set("100")
    assert(printer_value.get_max()) == "100"

    # act
    printer_value.set("110")

    # assert
    assert(printer_value.get_max()) == "110"


def test_set_max_kept_on_lower_value():
    # arrange
    printer_value = PrinterModelValue()
    printer_value.set("100")
    assert(printer_value.get_max()) == "100"

    # act
    printer_value.set("80")

    # assert
    assert(printer_value.get_max()) == "100"


def test_set_min_initial_ok():
    # arrange
    printer_value = PrinterModelValue()
    assert(printer_value.get_min()) == "?"

    # act
    printer_value.set("100")

    # assert
    assert(printer_value.get_min()) == "100"


def test_set_min_second_time_ok():
    # arrange
    printer_value = PrinterModelValue()
    printer_value.set("100")
    assert(printer_value.get_min()) == "100"

    # act
    printer_value.set("90")

    # assert
    assert(printer_value.get_min()) == "90"


def test_set_min_kept_on_higher_value():
    # arrange
    printer_value = PrinterModelValue()
    printer_value.set("100")
    assert(printer_value.get_min()) == "100"

    # act
    printer_value.set("120")

    # assert
    assert(printer_value.get_min()) == "100"
