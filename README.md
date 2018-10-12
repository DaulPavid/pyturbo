PyTurbo
=======

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A simple implementation of turbo codes in Python.

This project has not been optimized for speed, and only implements a simple rate 1/3 code with no puncturing. I might make it more generic, or implement an optimized version in C, but this package should really only serve as a reference implementation. It was created for a short technical blog post on my [website](https://daulpav.id).

## About ##

Turbo codes are a class of error correction codes that are used in cellular communication standards (e.g. 3GPP LTE) and deep space communications.
With long enough codes, they can approach the theoretical capacity of a channel, and provide excellent performance for their decoding complexity.

## Getting Started ##

Take a look at the `examples` folder for visualizations and test inputs to the encoder and decoder.

To test things out quickly, install `venv`:

    $ [sudo] apt install python3-venv
    $ python3 -m venv pyvm
    $ source pyvm/bin/activate

Then, execute the following commands:

    $ git clone https://github.com/DaulPavid/pyturbo.git
    $ cd pyturbo
    $ python setup.py install
    $ cd examples
