#
# AWGN Channel
#

#!/usr/bin/env python3

import numpy as np 


class AWGN:
    @staticmethod
    def convert_to_symbols(vector):
        return np.add(np.multiply(vector, 2), -1)

    def __init__(self, noise_dB):
        self.scale = 1.0 / (10.0**(noise_dB / 20.0))

    def execute(self, vector):
        noise = np.random.normal(0, 1, len(vector))
        noise = np.multiply(noise, self.scale)
        return np.add(vector, noise)
