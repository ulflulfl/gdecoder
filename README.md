# gdecoder
Simple decode of 3D printer .gcode files, focussed on common x/y/z printer with a single extruder.

In an attempt to understand gcode details, I've started a simple python script that takes the gcode (text) file and adds human readable comments to it. In addition, if adds meta infos like the printed area and (common) filament types probably suitable (based on the temperatures used).

Special gcode features used e.g. for dual extruders, delta printers, resin printers or CNC mills are not implemented.

There are other similiar programs like: https://github.com/BarrensZeppelin/humanize-gcode/tree/master

Hint: Many gcode details can be found at:
* https://reprap.org/wiki/G-code
* https://marlinfw.org/meta/gcode/

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