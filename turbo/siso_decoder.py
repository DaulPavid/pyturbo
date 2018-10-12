#
# Soft Input Soft Output (SISO) Decoder
#

import math
import itertools
import numpy as np

from .trellis import Trellis


class SISODecoder:
    @staticmethod
    def init_branch_metrics(m, n, depth):
        return np.array(depth * [m * [n * [0.0]]])

    @staticmethod
    def init_path_metric(m, depth):
        matrix = np.array(depth * [m * [-math.inf]])
        matrix[:, 0] = 0
        return matrix

    @staticmethod
    def demultiplex(vector):
        result = list(zip(vector[0::3], vector[1::3], vector[2::3]))
        return [(x, y, 0.0) for x, y, _ in result]

    def __init__(self, block_size):
        self.trellis = Trellis()
        self.block_size = block_size

        self.reset()

    def reset(self):
        self.branch_metrics = self.init_branch_metrics(4, 4, self.block_size)

        self.forward_metrics = self.init_path_metric(4, self.block_size + 1)
        self.backward_metrics = self.init_path_metric(4, self.block_size + 1)

        self.LLR = np.zeros(self.block_size)

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

        self.forward_metrics[k, state] = self.trellis.butterfly(forward_metrics, branch_metrics)

    def compute_backward(self, k, state):
        future_states = self.trellis.future_states[state]

        r = self.block_size - k

        backward_metrics = self.backward_metrics[k - 1, future_states]
        branch_metrics = self.branch_metrics[r, state, future_states]

        self.backward_metrics[k, state] = self.trellis.butterfly(backward_metrics, branch_metrics)

    def compute_LLR(self, k):
        r = self.block_size - k - 1

        positive = []
        negative = []

        for transition in self.trellis.possible_transitions:
            m, n = transition
            i, _ = self.trellis.transition_to_symbols(m, n)

            forward_metric = self.forward_metrics[k, m]
            branch_metric = self.branch_metrics[k, m, n]
            backward_metric = self.backward_metrics[r, n]

            if i < 0:
                negative.append(forward_metric + branch_metric + backward_metric)
            else:
                positive.append(forward_metric + branch_metric + backward_metric)

        self.LLR[k] = np.max(positive) - np.max(negative)

    def execute(self, tuples):
        self.compute_branch(tuples)

        for k in range(1, self.block_size + 1):
            for state in range(0, 4):
                self.compute_forward(k, state)
                self.compute_backward(k, state)

        for k in range(0, self.block_size):
            self.compute_LLR(k)

        return self.LLR
