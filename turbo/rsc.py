#
# Recursive Systematic Encoder
#

import collections


class RSC:
    def __init__(self):
        self.registers = collections.deque([0, 0])

    def push(self, value):
        result = value ^ self.registers[-1]
        self.registers.rotate(1)
        self.registers[0] = result
        return result

    def execute(self, vector):
        return [self.push(v) for v in vector]
