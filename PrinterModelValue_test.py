from PrinterModelValue import PrinterModelValue


def test_get_InitialQuestionMark():
    # arrange
    printerValue = PrinterModelValue()

    # act
    value = printerValue.get()

    # assert
    assert(value) == "?"


def test_set_ValueOk():
    # arrange
    printerValue = PrinterModelValue()
    assert(printerValue.get()) == "?"

    # act / assert
    printerValue.set("100")
    assert(printerValue.get()) == "100"


def test_set_MaxInitialOk():
    # arrange
    printerValue = PrinterModelValue()
    assert(printerValue.getMax()) == "?"

    # act
    printerValue.set("100")

    # assert
    assert(printerValue.getMax()) == "100"


def test_set_MaxSecondTimeOk():
    # arrange
    printerValue = PrinterModelValue()
    printerValue.set("100")
    assert(printerValue.getMax()) == "100"

    # act
    printerValue.set("110")

    # assert
    assert(printerValue.getMax()) == "110"


def test_set_MaxKeptOnLowerValue():
    # arrange
    printerValue = PrinterModelValue()
    printerValue.set("100")
    assert(printerValue.getMax()) == "100"

    # act
    printerValue.set("80")

    # assert
    assert(printerValue.getMax()) == "100"


def test_set_MinInitialOk():
    # arrange
    printerValue = PrinterModelValue()
    assert(printerValue.getMin()) == "?"

    # act
    printerValue.set("100")

    # assert
    assert(printerValue.getMin()) == "100"


def test_set_MinSecondTimeOk():
    # arrange
    printerValue = PrinterModelValue()
    printerValue.set("100")
    assert(printerValue.getMin()) == "100"

    # act
    printerValue.set("90")

    # assert
    assert(printerValue.getMin()) == "90"


def test_set_MinKeptOnHigherValue():
    # arrange
    printerValue = PrinterModelValue()
    printerValue.set("100")
    assert(printerValue.getMin()) == "100"

    # act
    printerValue.set("120")

    # assert
    assert(printerValue.getMin()) == "100"
