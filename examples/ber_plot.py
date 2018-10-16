#
# Bit Error Rate Performance Plot
#

#!/usr/bin/env python3

import argparse
import random
import numpy as np
import matplotlib.pyplot as plot

from turbo import TurboEncoder
from turbo import AWGN
from turbo import TurboDecoder
from turbo import SISODecoder


def create_ber_plot(plot_params):
    block_size = plot_params["block_size"]
    num_trials = plot_params["num_trials"]

    snr_range = np.linspace(*plot_params["snr"])

    interleaver = random.sample(range(0, block_size), block_size)
    encoder = TurboEncoder(interleaver)
    decoder = TurboDecoder(interleaver)

    num_errors = np.zeros(len(snr_range))

    for n in range(len(snr_range)):
        for _ in range(num_trials):
            input_vector = np.random.randint(2, size=block_size)
            encoded_vector = encoder.execute(input_vector)

            channel = AWGN(snr_range[n])

            channel_vector = list(map(float, encoded_vector))
            channel_vector = channel.convert_to_symbols(channel_vector)

            channel_vector = channel.execute(channel_vector)

            decoded_vector = decoder.execute(channel_vector)
            decoded_vector = [int(b > 0.0) for b in decoded_vector]

            decoder.reset()

            error_count = sum([x ^ y for x, y in zip(input_vector, decoded_vector)])
            num_errors[n] = num_errors[n] + error_count

        print("Finished {} trials for SNR = {:8.2f} dB ...".format(num_trials, snr_range[n]))

    ber_values = num_errors / (num_trials * block_size)

    plot.plot(snr_range, ber_values, "r.-")
    plot.yscale("log")
    plot.title("Turbo Codes Performance for R=1/3, Trials={}".format(num_trials))
    plot.xlabel("SNR [dB]")
    plot.ylabel("Bit Error Rate (BER)")
    plot.grid(b=True, which="major", linestyle="-")
    plot.grid(b=True, which="minor", linestyle="--")
    plot.show()


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--snr", nargs=3, type=float,
        default=[-10.0, 10.0, 20],
        help="SNR range [dB] in an AWGN channel"
    )
    parser.add_argument(
        "--block-size", type=int,
        default=40,
        help="Block size (size of interleaver)"
    )
    parser.add_argument(
        "--num-trials", type=int,
        default=50,
        help="Number of trials to run BER simulation"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = options()
    plot_params = {
        "snr": args.snr,
        "block_size": args.block_size,
        "num_trials": args.num_trials
    }
    create_ber_plot(plot_params)
