#
# AWGN Channel Plot
#

#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plot

from turbo import AWGN


def create_awgn_plot(input_vector, SNR_dB):
    channel = AWGN(SNR_dB)
    input_vector = list(map(float, input_vector))
    input_vector = channel.convert_to_symbols(input_vector)

    plot.subplot(1, 2, 1)
    plot.plot(input_vector, 'b.')
    plot.title("Input Vector (BPSK)")

    output_vector = channel.execute(input_vector)

    plot.subplot(1, 2, 2)
    plot.plot(output_vector, 'r.')
    plot.title("Channel Output (BPSK + AWGN)")
    plot.show()


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--snr", type=float,
        default=5.0,
        help="SNR [dB] in an AWGN channel"
    )
    parser.add_argument(
        "-i", "--input", nargs="+", type=int,
        default=10 * [1, 1, 0, 0, 1, 0, 1, 0, 1, 1],
        help="Input vector to the AWGN channel"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = options()
    create_awgn_plot(args.input, args.snr)
