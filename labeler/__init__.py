from functools import partial
from typing import Callable
from contents.skin.labler import SkinPatcher


def get_labeler_fn(labeler, **kwargs) -> Callable:
    return labeler(**kwargs)


REGISTRY = {'SkinPatcher': partial(get_labeler_fn, labeler=SkinPatcher),
            }
