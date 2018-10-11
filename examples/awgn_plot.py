#
# AWGN Channel Plot
#

#!/usr/bin/env python3

import matplotlib.pyplot as plot

from turbo import AWGN


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
