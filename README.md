# rule-generator
A python module for simulating one-dimensional cellular automata rules.

## Introduction
[One dimensional elementary cellular automata](http://mathworld.wolfram.com/ElementaryCellularAutomaton.html) are cells on a coloured grid that discretely and simultaneuosly evolve based on their surrounding cells. For more information and conventions please refer to the MathWorld article; in particular, please make sure to understand how the rules are named and how they work. rulegenerator.py is a python module which provides functions and a command line interface for generating these elementary cellular automata.

## Usage

#### Functions

There are two functions to generate the grid for a rule:
* generate_rule(generations, initial_config, rule_num)
* generate_rule_wrap(generations, initial_config, rule_num, wrap_width)

Both of these functions return a list where each element of the list is a deque (qhich may be converted to a list at any time using the list() function). Each of the deques represents a generation in the automata evolution in increasing order. The deques may be assumed to all have equal sizes. The difference between these two functions is how the grid is represented.
In `generate_rule` the grid is infinite, starting out with all 0 cells, and the cells will freely expand in any direction. In `generate_rule_wrap` the grid is finite and the edges wrap around to one another. For example, a cell at the left edge of the grid will consider a cell on the same row on the right edge of the grid to be its left neighbour. The `wrap_width` parameter is used to specify the width of the grid in this case. This integer must be an odd number. Excluding `wrap_width`, the rest of the arguments are identical for both functions. `generations` is the number of generations (an integer) that the grid is to be simulated; this will be identical to the length of the returned list. `initial_config` is a string and is meant to represent the starting state of the automaton. The string must be at least 3 characters in length and an odd number. Represent the state using a binary number such as `010`. `rule_num` is the rule that the grid is supposed to follow, to be entered as an integere from 0 to 255. [Read this article for more information on rules](http://plato.stanford.edu/entries/cellular-automata/supplement.html).

There are also two functions that can work with the lists that are returned by `generate_rule` and `generate_rule_wrap`:
* fix_width(grid, width)
adjust the width of the entered `grid` (a list of deques from `generate_rule` or `generate_rule_wrap`) to `width`

* to_image(grid, path)
save the `grid` to the specified path as a PNG image where each 0 cell is a white pixel and each 1 cell is a black pixel. **PIL [(Pillow)](https://github.com/python-pillow/Pillow) must be installed to use this function**.

#### Terminal

rulegenerator.py may also be used as a command line script/program to generate images of elementary cellular automata simulations. **PIL [(Pillow)](https://github.com/python-pillow/Pillow) must be installed to use rulegenerator this way**.
Use by typing:
```rulegenerator.py -i <initial configuration> -r <desired rule as an integer> -g <number of generations to compute> -o <name and path for output image> [--fixedwidth <width> --wrapped <width>]```
or:
```python rulegenerator.py -i <initial configuration> -r <desired rule as an integer> -g <number of generations to compute> -o <name and path for output image> [--fixedwidth <width> --wrapped <width>]```
in your command window.

* -i: The initial configuration (generation 0) of the automata as a binary number. Must have odd length or will be extended.
* -r: The rule for the cellular automata evolution as an integer from 0 to 255.
* -g: Number of generations to evolve the automata. This will specify the height (in pixels) of the output image.
* -o: Specify the name and location of the output image.
* --fixedwidth: Force the output image to have the specified width (in pixels). The width must be an odd-numbered integer. If it is not odd it will be rounded up to the next odd number.
* --wrapped: Make the grid have the specified width (in pixels) and wrap around instead of being infinite. The width must be an odd-numbered integer or it will be rounded up to the next odd number. Will override --fixedwidth.

Use the `-h` flag to bring up these instructions.

## Requirements
Python 3 and [Pillow](https://github.com/python-pillow/Pillow) (Pillow only required for the command line and `to_image` features).
