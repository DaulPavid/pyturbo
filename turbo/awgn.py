#
# AWGN Channel
#

#!/usr/bin/env python3

import numpy as np 
import matplotlib.pyplot as plot


class AWGN:
    @staticmethod
    def convert_to_symbols(vector):
        return np.add(np.multiply(vector, 2), -1)

    def __init__(self, noise_dB):
        self.scale = 1.0 / (10.0**(noise_dB / 10.0))

    def execute(self, vector):
        noise = np.random.normal(0, 1, len(vector))
        noise = np.multiply(noise, self.scale)
        return np.add(vector, noise)


if __name__ == "__main__":
    channel = AWGN(2)
    input_vector = 10 * [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    input_vector = list(map(float, input_vector))
    input_vector = channel.convert_to_symbols(input_vector)

    plot.subplot(1, 2, 1)
    plot.plot(input_vector, 'b.')
    plot.title("input_vector")

    output_vector = channel.execute(input_vector)

    plot.subplot(1, 2, 2)
    plot.plot(output_vector, 'r.')
    plot.title("output_vector")
    plot.show()
