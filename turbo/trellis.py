#
# Trellis Object
#

import itertools
import numpy as np


class Trellis:
    @staticmethod
    def butterfly(path_metrics, branch_metrics):
        result = [path + branch for path, branch in zip(path_metrics, branch_metrics)]
        return np.max(result)

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
        return self.transition_matrix[state, next_state]
