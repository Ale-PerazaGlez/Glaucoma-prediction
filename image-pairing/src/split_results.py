from numpy.random import permutation
from numpy import dtype, split
import numpy as np


def train_test_split(data, rate=0.3):
    shuffled_data = permutation((np.array(data, dtype=object)))
    data_length = shuffled_data.shape[0]
    results = split(shuffled_data, [int(rate * data_length), data_length])
    train_data = list(results[1])
    test_data = list(results[0])
    return train_data, test_data
