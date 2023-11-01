import copy
import os
import torch
import random
from runner.base import Base
from typing import Callable, Iterable


class ImageTorchRunner(Base):
    def __init__(self, input_path: str, output_path: str, labeler: Callable, model: Callable, **kwargs):
        super().__init__(input_path, output_path, labeler, model, **kwargs)

    def _get_sampler(self, **kwargs) -> Iterable:
        sampler = []
        input_path = kwargs['input_path']
        files = os.listdir(input_path)
        begin = 0
        if self.resume:
            exists = os.listdir(self.output_path)
            last = torch.load(os.path.join(self.output_path, exists[-1]))
            begin = files.index(last['input_path'].replace(input_path + '\\', ''))

        for index in range(begin, len(files)):
            image_name = files[index]
            tup = (index, os.path.join(input_path, image_name))
            sampler.append(copy.deepcopy(tup))

        if self.shuffle:
            random.shuffle(sampler)
        if self.length > 0:
            sampler = sampler[:self.length]
        return sampler

    def _close(self) -> str:
        pass
