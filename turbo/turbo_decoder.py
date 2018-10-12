#
# Turbo Decoder
#

import numpy as np

from .siso_decoder import SISODecoder


class TurboDecoder:
    @staticmethod
    def demultiplex(a, b, extrinsic):
        return list(zip(a, b, extrinsic))

    @staticmethod
    def early_exit(LLR, LLR_ext):
        LLR = [int(s > 0) for s in LLR]
        LLR_ext = [int(s > 0) for s in LLR_ext]
        return LLR == LLR_ext

    def __init__(self, interleaver, num_registers=2, max_iter=16):
        self.interleaver = interleaver
        self.block_size = len(self.interleaver)
        self.num_registers = num_registers
        self.decoders = 2 * [SISODecoder(self.block_size + num_registers)]
        self.max_iter = max_iter

    def interleave(self, vector):
        interleaved = np.zeros(len(vector), dtype=int)
        for i in range(0, self.block_size):
            interleaved[i] = vector[self.interleaver[i]]

        return interleaved

    def deinterleave(self, vector):
        deinterleaved = np.zeros(len(vector), dtype=int)
        for i in range(0, self.block_size):
            deinterleaved[self.interleaver[i]] = vector[i]

        return deinterleaved

    def execute(self, vector):
        LLR_ext = np.zeros(self.block_size + self.num_registers, dtype=float)

        for _ in range(self.max_iter):
            input_tuples = self.demultiplex(vector[::3], vector[1::3], LLR_ext)

            LLR_1 = self.decoders[0].execute(input_tuples)
            LLR_1 = LLR_1 - LLR_ext - 2 * vector[::3]
            LLR_interleaved = self.interleave(LLR_1)

            input_interleaved = self.interleave(vector[::3])

            input_tuples = self.demultiplex(input_interleaved, vector[2::3], LLR_interleaved)

            LLR_2 = self.decoders[1].execute(input_tuples)
            LLR_2 = LLR_2 - LLR_interleaved - 2 * vector[::3]
            LLR_ext = self.deinterleave(LLR_2)

            if self.early_exit(LLR_1, LLR_ext):
                break

        return LLR_ext
