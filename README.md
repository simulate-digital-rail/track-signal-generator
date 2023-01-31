# Track-signal-generator

Used to generate Block signals for [yaramo](https://github.com/simulate-digital-rail/yaramo) tracks.

## Setup

This project uses [poetry](https://python-poetry.org/) for dependency-management. After cloning, install the dependencies using `poetry install`.

## Example

To see the generator in action, take a look at `example/example1.py`. To install all the required dependencies, use `poetry install --with example`. After that, you can run the example using `poetry run python example/example1.py`. It will generate a SUMO-Export with a straight track of the length 1001 m.

## Implementation-state & potential issues

Signals will be placed on edges with no regards if there are signals already existing there. Additionally, if a signal is placed directly in front of a node, a new signal will be placed at that node for a beginning edge.
Signals will also overlap add switches, as two edges begin there.
