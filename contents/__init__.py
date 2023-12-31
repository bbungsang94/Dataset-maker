from functools import partial
from typing import Callable

from contents.base import RandomGenerator
from contents.skin.model import Patcher, Editor


def get_model_fn(model, **kwargs) -> Callable:
    return model(**kwargs)


REGISTRY = {'SkinPatcher': partial(get_model_fn, model=Patcher),
            'SkinEditor': partial(get_model_fn, model=Editor),
            'RandomGenerator': partial(get_model_fn, model=RandomGenerator),
            }