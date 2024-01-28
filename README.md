# gdecoder

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=white) ![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white) [![python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org) [![codecov](https://codecov.io/gh/ulflulfl/gdecoder/graph/badge.svg?token=3E8MW86VM7)](https://codecov.io/gh/ulflulfl/gdecoder) [![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Simple decode of 3D printer .gcode files, focused on common x/y/z printer with a single extruder.

In an attempt to understand G-code details, I've started a python script that takes a .gcode (text) file and adds human readable comments to it. In addition, it adds summary infos like the printed area and (common) filament types probably suitable for the print (based on the temperatures used).

Special G-code features e.g. for dual extruders, delta printers, resin printers or CNC mills are not implemented.

There are other similiar programs like: https://github.com/BarrensZeppelin/humanize-gcode/tree/master

Hint: Many G-ccode details can be found at:
* https://en.wikipedia.org/wiki/G-code
* https://reprap.org/wiki/G-code
* https://marlinfw.org/meta/gcode/

## Usage

Clone or download the repository.

Common usage:

```
gdecoder -i examples_synthetic/generic.gcode
```
(showing a synthetic example .gcode)

For a list of available options:

```
gdecoder -h
```



## Tests

Automated tests can be found in the GitHub Actions, including: flake8 (lint), pytest and coverage (pushed to https://app.codecov.io/gh/ulflulfl/gdecoder).

There seems to be many ways to manually start pytest, this is what works for me ...

Test run:
```
python -m pytest
```
Test run with coverage in html format:
```
python -m pytest --cov=. --cov-report html
```

Don't forget to install pytest and pytest-cov!