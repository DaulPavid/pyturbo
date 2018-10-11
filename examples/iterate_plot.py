#
# Log-likelihood Ratio Plot
# Illustrates how the decoder improves its confidence
#

#!/usr/bin/env python3

import matplotlib.pyplot as Plot

from turbo import TurboEncoder
from turbo import AWGN
from turbo import TurboDecoder


def create_ber_plot(input_vector, SNR_dB):
    pass


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
    parser.add_argument(
        "-r", "--rate", type=int,
        default=3,
        help="Setting a rate 1/r code"
    )
    return parser.parse_args()


if __name__ == "__main__":
    pass
