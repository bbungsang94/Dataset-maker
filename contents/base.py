import torch
import numpy as np


class RandomGenerator:
    def __init__(self, size=1, scale=1, offset=1):
        self.size = size
        self.scale = scale
        self.offset = offset

    def __call__(self, *args):

        return {'value': torch.from_numpy(np.random.rand(1, self.size) * self.scale + self.offset)}
