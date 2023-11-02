from runner.base import Base
from typing import Callable, Iterable


class EmptyRunner(Base):
    def __init__(self, input_path: str, output_path: str, labeler: Callable, model: Callable, **kwargs):
        super().__init__(input_path, output_path, labeler, model, **kwargs)

    def _get_sampler(self, **kwargs) -> Iterable:
        return range(kwargs['length'])

    def _close(self) -> str:
        pass
