# test gdecoder.py with some example files
from gdecoder import gdecoder
from gdecoder import parse_args
import pathlib
import pytest
pytestmark = pytest.mark.integration


def create_args_emulation_with_defaults(input_file):
    class ArgsEmulation:
        pass
    ArgsEmulation.input = str(input_file)

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
    if "synthetic_input_file" in metafunc.fixturenames:
        metafunc.parametrize("synthetic_input_file", pathlib.Path().glob("./examples_synthetic/*.gcode"))


def test_gcode_in_examples_synthetic_folder(synthetic_input_file):
    args_emulation = create_args_emulation_with_defaults(synthetic_input_file)
    args_emulation.showVerbose = True
    gdecoder(args_emulation)


def test_parser_all_optional_parameters_unused():
    parser = parse_args(['-i', 'abc'])

    assert(parser.input == "abc")
    assert(parser.hideSummary is False)
    assert(parser.hideComments is False)
    assert(parser.hideGCode is False)
    assert(parser.hideDecoded is False)
    assert(parser.showVerbose is False)
    assert(parser.stopOnUndecoded is False)


def test_parser_all_optional_parameters_used():
    parser = parse_args(['-i', 'abc', "-s", "-c", "-g", "-d", "-v", "-u"])

    assert(parser.input == "abc")
    assert(parser.hideSummary is True)
    assert(parser.hideComments is True)
    assert(parser.hideGCode is True)
    assert(parser.hideDecoded is True)
    assert(parser.showVerbose is True)
    assert(parser.stopOnUndecoded is True)
