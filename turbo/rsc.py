#
# Recursive Systematic Encoder
#

import numpy as np
import collections


class RSC:
    def __init__(self):
        self.reset()

    def reset(self):
        self.registers = collections.deque([0, 0])

    def push(self, value):
        result = value ^ self.registers[-1]
        self.registers.rotate(1)
        self.registers[0] = result
        return result

    def terminate(self):
        result = self.registers[-1]
        self.registers.rotate(1)
        self.registers[0] = 0
        return result

    def execute(self, vector):
        result = np.zeros(len(vector) + len(self.registers))

        result[:len(vector):] = [self.push(v) for v in vector]
        result[len(vector)::] = [self.terminate() for _ in range(len(self.registers))]

        systematic = np.concatenate((vector, result[len(vector)::]))
        return result, systematic
