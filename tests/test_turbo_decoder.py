#
# Turbo Decoder Unit Tests
#

import unittest

from turbo import TurboEncoder
from turbo import AWGN
from turbo import SISODecoder


def test_rsc_encoder():
    rsc = RSC()

    input_vector = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    output_vector = rsc.execute(input_vector)

    registers = rsc.registers

    print("input_vector = {}".format(input_vector))
    print("output_vector = {}".format(output_vector))
    print("state = {}".format(registers))


def test_turbo_encoder()
    interleaver = [9, 8, 5, 6, 2, 1, 7, 0, 3, 4]
    turbo_encoder = TurboEncoder(interleaver)

    input_vector = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    output_vector = turbo_encoder.execute(input_vector)

    print("output = {}".format(output_vector))

    assert(3 * len(input_vector) == len(output_vector))


def test_siso_decoder():
    channel = AWGN(20)
    encoder = TurboEncoder()
    decoder = SISODecoder()

    input_vector = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    encoded_vector = encoder.execute(input_vector)

    encoded_vector = list(map(float, encoded_vector))
    channel_vector = channel.convert_to_symbols(encoded_vector)

    channel_vector = channel.execute(channel_vector)

    channel_vector = decoder.demultiplex(channel_vector)
    channel_vector = [(x, y, 0.0) for x, y, _ in channel_vector]

    decoded_vector = decoder.execute(channel_vector)
    decoded_vector = [int(b > 0.0) for b in decoded_vector]

    print("input_vector = {}".format(input_vector))
    print("encoded_vector = {}".format(encoded_vector))
    print("decoded_vector = {}".format(decoded_vector))

    assert(input_vector == decoded_vector)


if __name__ == "__main__":
    test_turbo_encoder()
