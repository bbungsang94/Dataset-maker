import copy
import os
from runner.base import Base
from typing import Callable, Iterable


class ImageTorchRunner(Base):
    def __init__(self, input_path: str, output_path: str, labeler: Callable, model: Callable, **kwargs):
        super().__init__(input_path, output_path, labeler, model, **kwargs)

    def _get_sampler(self, **kwargs) -> Iterable:
        sampler = []
        input_path = kwargs['input_path']
        files = os.listdir(input_path)
        for index, image_name in enumerate(files):
            tup = (index, os.path.join(input_path, image_name))
            sampler.append(copy.deepcopy(tup))
        return sampler

    def _close(self) -> str:
        pass
