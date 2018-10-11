#
# Turbo Decoder Unit Tests
#

import unittest

from turbo import RSC
from turbo import TurboEncoder
from turbo import AWGN
from turbo import SISODecoder


class TestEncoder(unittest.TestCase):
    def test_rsc_encoder(self):
        rsc = RSC()

        input_vector = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
        output_vector = rsc.execute(input_vector)

        registers = rsc.registers

        print("input_vector = {}".format(input_vector))
        print("output_vector = {}".format(output_vector))
        print("state = {}".format(registers))

        self.assertEqual(len(input_vector), len(output_vector))

    def test_turbo_encoder(self):
        interleaver = [9, 8, 5, 6, 2, 1, 7, 0, 3, 4]
        turbo_encoder = TurboEncoder(interleaver)

        input_vector = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
        output_vector = turbo_encoder.execute(input_vector)

        print("output = {}".format(output_vector))

        self.assertEqual(3 * len(input_vector), len(output_vector))


class TestTurboDecoder(unittest.TestCase):
    def test_siso_decoder(self):
        interleaver = [9, 8, 5, 6, 2, 1, 7, 0, 3, 4]
        encoder = TurboEncoder(interleaver)

        channel = AWGN(20)
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

        self.assertEqual(input_vector, decoded_vector)


if __name__ == "__main__":
    unittest.main()
