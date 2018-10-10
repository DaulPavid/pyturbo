PyTurbo
=======

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A simple implementation of a turbo decoder in Python. This repository is meant to serve as a example of how a turbo decoder is implemented in software, and provide a few visualizations and plots. It is not optimized in any way.

## About ##

Turbo codes are a class of error correction codes that are used in cellular communication standards like LTE, and deep space communications.
With long enough codes, they can approach the theoretical capacity of a channel, and provide excellent performance for their decoding complexity.
I wrote a [blog post](https://ofdm.io) about turbo codes and understanding them from an implementation point of view. This project was written for that post.

## Getting Started ##

Take a look at the examples folder for visualizations and test inputs to the encoder and decoder.