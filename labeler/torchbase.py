from abc import ABCMeta
from labeler.base import Base as Labeler
import torch


class Base(Labeler, metaclass=ABCMeta):
    def save(self, output: dict, save_path: str):
        torch.save(output, save_path)
