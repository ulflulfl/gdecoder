# test gdecoder.py with some example files
from gdecoder import gdecoder
import pathlib


def createArgsEmulationWithDefaults(inputFile):
    class ArgsEmulation:
        pass
    ArgsEmulation.input = str(inputFile)

    # settings for maximum output -> crashes becomes most likely in the test
    ArgsEmulation.stopOnUndecoded = True
    ArgsEmulation.hideComments = False
    ArgsEmulation.hideGCode = False
    ArgsEmulation.hideDecoded = False
    ArgsEmulation.hideSummary = False

    # using verbose is very slow when using "real world" gcode files -> don't show by default
    ArgsEmulation.showVerbose = False
    return ArgsEmulation


# test all .gcode files in the examples_synthetic folder
def pytest_generate_tests(metafunc):
    if "synthetic_inputFile" in metafunc.fixturenames:
        metafunc.parametrize("synthetic_inputFile", pathlib.Path().glob("./examples_synthetic/*.gcode"))


def test_gcode_in_examples_synthetic_folder(synthetic_inputFile):
    ArgsEmulation = createArgsEmulationWithDefaults(synthetic_inputFile)
    ArgsEmulation.showVerbose = True
    gdecoder(ArgsEmulation)
