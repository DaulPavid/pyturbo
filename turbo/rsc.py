#
# Recursive Systematic Encoder
#

#!/usr/bin/env python3

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


if __name__ == "__main__":
    rsc = RSC()
    input_vector = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]

    print("input_vector = {}".format(input_vector))
    print("output_vector = {}".format(rsc.execute(input_vector)))
    print("state = {}".format(rsc.registers))