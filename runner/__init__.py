from functools import partial
from runner.base import Base
from runner.vision import ImageTorchRunner


def get_runner_fn(runner, **kwargs) -> Base:
    return runner(**kwargs)


REGISTRY = {'torch': partial(get_runner_fn, runner=ImageTorchRunner),
            }