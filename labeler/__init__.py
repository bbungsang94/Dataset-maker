from functools import partial
from typing import Callable

from contents.ftm.labeler import GraphLabeler
from contents.skin.labler import SkinPatcher
from contents.stm.labeler import SMPLLabeler


def get_labeler_fn(labeler, **kwargs) -> Callable:
    return labeler(**kwargs)


REGISTRY = {'SkinPatcher': partial(get_labeler_fn, labeler=SkinPatcher),
            'SMPLLabeler': partial(get_labeler_fn, labeler=SMPLLabeler),
            'FLAMELabeler': partial(get_labeler_fn, labeler=GraphLabeler),
            }
