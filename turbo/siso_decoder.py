#
# Soft Input Soft Output (SISO) Decoder
#

import math
import itertools
import numpy as np

from turbo_encoder import TurboEncoder
from awgn import AWGN


def butterfly(path_metrics, branch_metrics):
    result = [path + branch for path, branch in zip(path_metrics, branch_metrics)]
    return np.amax(result)


class Trellis:
    def __init__(self):
        self.transition_matrix = np.array(
                                  [[(-1, -1), None, (1, 1), None],
                                  [(1, -1), None, (-1, 1), None],
                                  [None, (-1, -1), None, (1, 1)],
                                  [None, (1, -1), None, (-1, 1)]])

        self.past_states = [(0, 1), (2, 3), (0, 1), (2, 3)]
        self.future_states = [(0, 2), (0, 2), (1, 3), (1, 3)]

        all_transitions = list(itertools.product([0, 1, 2, 3], repeat=2))
        self.possible_transitions = [t for t in all_transitions if self.transition_matrix[t] is not None]

    def transition_to_symbols(self, state, next_state):
        return self.transition_matrix[state][next_state]


class SISODecoder:
    @staticmethod
    def init_branch_metrics(m, n, depth):
        return np.array(depth * [m * [n * [None]]])

    @staticmethod
    def init_path_metric(m, depth):
        matrix = np.array(depth * [m * [-math.inf]])
        matrix[:, 0] = 0
        return matrix

    @staticmethod
    def demultiplex(vector):
        return list(zip(vector[0::3], vector[1::3], vector[2::3]))

    def __init__(self):
        self.trellis = Trellis()
        self.block_size = 10

        self.branch_metrics = self.init_branch_metrics(4, 4, self.block_size)

        self.forward_metrics = self.init_path_metric(4, self.block_size + 1)
        self.backward_metrics = self.init_path_metric(4, self.block_size + 1)

        self.LLR = self.block_size * [None]

    def compute_branch(self, tuples):
        for k in range(0, self.block_size):
            for transition in self.trellis.possible_transitions:
                m, n = transition
                i, o = self.trellis.transition_to_symbols(m, n)

                self.branch_metrics[k, m, n] = i * tuples[k][0] + o * tuples[k][1] + i * tuples[k][2]

    def compute_forward(self, k, state):
        past_states = self.trellis.past_states[state]

        forward_metrics = self.forward_metrics[k - 1, past_states]
        branch_metrics = self.branch_metrics[k - 1, past_states, state]

        self.forward_metrics[k, state] = butterfly(forward_metrics, branch_metrics)

    def compute_backward(self, k, state):
        future_states = self.trellis.future_states[state]

        r = self.block_size - k

        backward_metrics = self.backward_metrics[k - 1, future_states]
        branch_metrics = self.branch_metrics[r, state, future_states]

        self.backward_metrics[k, state] = butterfly(backward_metrics, branch_metrics)

    def compute_LLR(self, k):
        r = self.block_size - k - 1

        positive = []
        negative = []

        for transition in self.trellis.possible_transitions:
            m, n = transition
            i, o = self.trellis.transition_to_symbols(m, n)

            forward_metric = self.forward_metrics[k, m]
            branch_metric = self.branch_metrics[k, m, n]
            backward_metric = self.backward_metrics[r, n]

            if i < 0:
                negative.append(forward_metric + branch_metric + backward_metric)
            else:
                positive.append(forward_metric + branch_metric + backward_metric)

        self.LLR[k] = np.amax(positive) - np.amax(negative)

    def execute(self, tuples):
        self.compute_branch(tuples)

        for k in range(1, self.block_size + 1):
            for state in range(0, 4):
                self.compute_forward(k, state)
                self.compute_backward(k, state)

        for k in range(0, self.block_size):
            self.compute_LLR(k)

        return self.LLR
