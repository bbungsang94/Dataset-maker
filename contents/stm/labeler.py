import numpy as np

from contents.stm.

output['output_path'] = self.output_path
desc = self._labeler(**output)

class SMPLLabeler():
    def __init__(self):
        pass

    def __call__(self, shape):
        pass

    def _get_poses(self):
        t = np.zeros((1, 55, 3))
        standing = np.zeros((1, 55, 3))
        hands = np.zeros((1, 55, 3))
        curve = get_curve(batch_size=1)
        sitting = np.zeros((1, 55, 3))
