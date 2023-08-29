import os
from abc import ABCMeta, abstractmethod
from typing import Iterable, Callable
from tqdm import tqdm


class Base(metaclass=ABCMeta):
    def __init__(self, input_path: str, output_path: str, labeler: Callable, model: Callable, **kwargs):
        kwargs['input_path'] = input_path
        exists = os.listdir(output_path)
        self.output_path = output_path
        self.resume = False
        self.length, self.count = 0, 0
        self.shuffle = False
        if 'length' in kwargs:
            self.length = kwargs['length']
        if 'shuffle' in kwargs:
            self.shuffle = kwargs['shuffle']
        if len(exists) > 0:
            self.resume = False

        self._sampler = self._get_sampler(**kwargs)
        self._labeler = labeler
        self._model = model

    @abstractmethod
    def _get_sampler(self, **kwargs) -> Iterable:
        pass

    @abstractmethod
    def _close(self) -> str:
        pass

    def loop(self):
        pbar = tqdm(self._sampler, desc="Beginning process", position=0, leave=False)
        for sample in pbar:
            output = self._model(sample)
            if output is None:
                continue
            output['output_path'] = self.output_path
            desc = self._labeler(**output)
            if desc:
                pbar.set_description(desc)

        return self._close()
