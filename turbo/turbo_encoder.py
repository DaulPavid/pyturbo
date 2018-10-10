#
# Turbo Encoder
#

from rsc import RSC


class TurboEncoder:
    def __init__(self, interleaver):
        self.interleaver = interleaver
        self.block_size = len(self.interleaver)
        self.encoders = [RSC(), RSC()]

    def interleave(self, vector):
        interleaved = [0 for _ in range(len(self.interleaver))]
        for i in range(0, self.block_size):
            interleaved[i] = vector[self.interleaver[i]]

        return interleaved

    def execute(self, vector):
        if not (len(vector) % self.block_size):
            raise ValueError(""" Turbo encoder expects vector size to be a
                                 multiple of the interleaver (block size) """)

        interleaved = self.interleave(vector)

        output = [None] * (3 * self.block_size)

        output[::3] = vector
        output[1::3] = self.encoders[0].execute(vector)
        output[2::3] = self.encoders[1].execute(interleaved)

        return output
