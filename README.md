# Caravel Remote

Remotely accessing [Caravel](https://github.com/efabless/caravel) GPIO pins through HKSPI to assist with debugging and bringup of a chip

- `caravel.py` - Code for interfacing with the Caravel HKSPI using PyFTDI to access internal housekeeping registers
- `gpio.py` - Code for configuring GPIO cells to feed inputs and monitor outputs via HKSPI
- `util.py` - Utility functions for bit manipulation
- `tiny_user_project_test.ipynb` - An example notebook for use with `tiny_user_project` style designs
