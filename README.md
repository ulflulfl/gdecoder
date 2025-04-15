# gdecoder

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=white) ![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white) [![Python versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org) [![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

![Python tests](https://github.com/ulflulfl/gdecoder/actions/workflows/python-tests.yml/badge.svg) [![codecov](https://codecov.io/gh/ulflulfl/gdecoder/graph/badge.svg?token=3E8MW86VM7)](https://app.codecov.io/gh/ulflulfl/gdecoder) ![Python lint](https://github.com/ulflulfl/gdecoder/actions/workflows/python-lint.yaml/badge.svg) ![md-linkcheck](https://github.com/ulflulfl/gdecoder/actions/workflows/md-linkcheck.yaml/badge.svg) ![Spell check](https://github.com/ulflulfl/gdecoder/actions/workflows/spellcheck.yaml/badge.svg)

Simple decode of 3D printer .gcode files, focused on common x/y/z printer with a single extruder.

In an attempt to understand G-code details, I've started a python script that takes a .gcode (text) file and adds human readable comments to it. In addition, it adds summary infos like the printed area and (common) filament types probably suitable for the print (based on the temperatures used).

Special G-code features e.g. for dual extruders, delta printers, resin printers or CNC mills are not implemented.

There are other similar programs like: https://github.com/BarrensZeppelin/humanize-gcode/tree/master

Hint: Many G-code details can be found at:
* https://en.wikipedia.org/wiki/G-code
* https://reprap.org/wiki/G-code
* https://marlinfw.org/meta/gcode/

## Usage

Clone or download the repository.

Common usage:

```
gdecoder -i README.gcode
```
(showing a synthetic example .gcode)

For a list of available options:

```
gdecoder -h
```

## Example Output

Output from the minimalistic [README.gcode](README.gcode) example:

```
>gdecoder -i README.gcode
; example comment
G0 F3600 X77.699 Y82.347 Z0.3                  ; Rapid Move (no print), Feedrate: 3600 mm/min, X: 77.699 mm, Y: 82.347 mm, Z: 0.3 mm
G1 F1800 X78.492 Y81.741 Z10 E0.04979          ; Linear Move (print), Feedrate: 1800 mm/min, X: 78.492 mm, Y: 81.741 mm, Z: 10 mm, E: 0.04979 mm
G2 X108.779 Y112.969 I0.066 J-0.148 E5.12789   ; Clockwise Arc Move (print), X:108.779, Y:112.969, I (distant X): 0.066, J (distant Y): -0.148, E: 5.12789 mm
G3 X89.633 Y106.090 I2.341 J3.365 E4.62923     ; Counter-Clockwise Arc Move (print), X:89.633, Y:106.090, I (distant X): 2.341, J (distant Y): 3.365, E: 4.62923 mm
G21                                            ; Set Units to Millimeters
G28                                            ; Move to Origin (Home, often: X=0, Y=0; Z=0)
G90                                            ; Set to Absolute Positioning
G91                                            ; Set to Relative Positioning
G92 E0.0                                       ; Set Position, new extruder position: 0.0 mm
M82                                            ; Set extruder to absolute mode
M83                                            ; Set extruder to relative mode
M84                                            ; Stop idle hold (disable motors)
M106 S255                                      ; Fan On, Fan Speed: 255 (0-255)
M107                                           ; Fan Off
M109 S200                                      ; Set Extruder Temperature and Wait, Target: 200 °C
M117 Cooling down...                           ; Display Message: "Cooling down..."
M140 S60                                       ; Set Bed Temperature (Fast), Target: 60 °C
M190 S60                                       ; Wait for bed temperature to reach target temp, Target: 60 °C
M300 P300 S4000                                ; Play beep sound, duration: 300 ms, frequency: 4000 Hz
;------------------------------------------------------------------------------
;Summary:
;File
;  Name      : README.gcode
;  Size      : 311 bytes
;  Modified  : Sun Jan 28 05:13:00 2024
;  Lines     : 20
;  Longest   : 45 characters (without comment lines)
;  GCode     : 19 commands
;Generator
;  Line      :
;  Name      :
;  Flavor    :
;Printed
;  X         : 31.08 mm
;  Y         : 31.23 mm
;  Z         : 9.7 mm
;Temperature
;  Extruder  : 200 °C (max.)
;  Bed       : 60 °C (max.)
;  Fan       : 255 (max.)
;Filament
;  Length    : 5.13 mm
;  suitable
;  PLA       : 0.0-0.0 g, 0.0-0.0 €    1.75 mm/1kg: Length: 325-340 m/kg, Price: 15-30 €/kg, Nozzle: 180-230 °C, Bed: 20-80 °C (bed optional)
;  TPU       : 0.0-0.0 g, 0.0-0.0 €    1.75 mm/1kg: Length: 330-360 m/kg, Price: 17-50 €/kg, Nozzle: 190-260 °C, Bed: 25-70 °C
;  unsuitable
;  PETG      : 0.0-0.0 g, 0.0-0.0 €    1.75 mm/1kg: Length: 310-350 m/kg, Price: 17-30 €/kg, Nozzle: 220-250 °C, Bed: 50-90 °C (bed optional)
;  ABS       : 0.0-0.0 g, 0.0-0.0 €    1.75 mm/1kg: Length: 380-405 m/kg, Price: 15-30 €/kg, Nozzle: 230-270 °C, Bed: 80-110 °C
;  Nylon     : 0.0-0.0 g, 0.0-0.0 €    1.75 mm/1kg: Length: 330-360 m/kg, Price: 23-50 €/kg, Nozzle: 220-290 °C, Bed: 85-120 °C
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