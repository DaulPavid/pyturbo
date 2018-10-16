#
# Log-likelihood Ratio (LLR) Iteration Plot
# Illustrates how the decoder improves its confidence
#

#!/usr/bin/env python3

import argparse
import random
import numpy as np
import matplotlib.pyplot as plot

from turbo import TurboEncoder
from turbo import AWGN
from turbo import TurboDecoder


def create_ber_plot(plot_params):
    snr = plot_params["snr"]
    block_size = plot_params["block_size"]
    max_iter = plot_params["max_iter"]

    interleaver = random.sample(range(0, block_size), block_size)
    encoder = TurboEncoder(interleaver)
    decoder = TurboDecoder(interleaver)

    input_vector = np.random.randint(2, size=block_size)
    encoded_vector = encoder.execute(input_vector)

    channel = AWGN(snr)

    channel_vector = list(map(float, encoded_vector))
    channel_vector = channel.convert_to_symbols(encoded_vector)

    channel_vector = channel.execute(channel_vector)

    for i in range(max_iter):
        decoder.iterate(channel_vector)
        plot.plot(decoder.LLR_ext[:block_size], '.', label="Iteration {}".format(i+1))

    plot.title("Turbo Decoder Iterations")
    plot.ylabel("Soft Bits")
    plot.xlabel("Bits")
    plot.grid(b=True, which="major", linestyle="--")
    plot.legend()
    plot.show()


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--snr", type=float,
        default=2.0,
        help="SNR [dB] in an AWGN channel"
    )
    parser.add_argument(
        "--block-size", type=int,
        default=50,
        help="Block size (size of interleaver)"
    )
    parser.add_argument(
        "--max-iter", type=int,
        default=6,
        help="Maximum iterations to run the turbo decoder"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = options()
    plot_params = {
        "snr": args.snr,
        "block_size": args.block_size,
        "max_iter": args.max_iter
    }
    create_ber_plot(plot_params)
