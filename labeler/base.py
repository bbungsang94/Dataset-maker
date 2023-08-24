from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, **kwargs) -> str:
        pass

    @abstractmethod
    def save(self, output: dict, save_path: str):
        pass
