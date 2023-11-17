import copy
import json
import os

import numpy as np
import torch

from contents.stm.preprocess.convention import get_interactions
from contents.stm.model import SMPL
from contents.stm.poses.pose import get_curve, get_t, get_sitdown, get_standing, get_hands_on
from contents.stm.taylor import Taylor
from labeler.torchbase import Base


class SMPLLabeler(Base):
    def __init__(self, smpl_root, pin_root, circ_root):
        self.batch_size = 1
        self.count = 0
        male_path = os.path.join(smpl_root, "SMPLX_MALE.pkl")
        female_path = os.path.join(smpl_root, "SMPLX_FEMALE.pkl")
        self.male = SMPL(path=male_path)
        self.female = SMPL(path=female_path)
        self.offset = torch.from_numpy(np.zeros((self.batch_size, 3)))

        with open(os.path.join(pin_root, 'standing.json'), 'r', encoding='UTF-8-sig') as f:
            standing = json.load(f)
        with open(os.path.join(pin_root, 'sitting.json'), 'r', encoding='UTF-8-sig') as f:
            sitting = json.load(f)
        with open(os.path.join(circ_root, 'circumference.json'), 'r', encoding='UTF-8-sig') as f:
            circ_dict = json.load(f)
        self.taylor = Taylor(tape=get_interactions(), pin=(standing, sitting), circ_dict=circ_dict)

    def __call__(self, **kwargs):
        shape = kwargs['value']
        gender = np.random.choice(2, 1)
        gender = "male" if gender > 0 else "female"

        poses = self._get_poses(batch_size=self.batch_size)
        models = dict()
        for key, value in poses.items():
            if gender == "male":
                v, _ = self.male(beta=shape, pose=value, offset=self.offset)
            else:
                v, _ = self.female(beta=shape, pose=value, offset=self.offset)
            models[key] = copy.deepcopy(v)

        self.taylor.update(model_dict=models)
        measure = self.taylor.order(gender=[gender], fast=False, visualize=False)
        measure = measure / measure.max()
        result = {
            'input': {
                'gender': gender,
                'shape': shape
            },
            'output': {
                'measure': measure
            }
        }
        self.save(result, os.path.join(kwargs['output_path'], "%06d.pth" % self.count))
        self.count += 1
        return None

    @staticmethod
    def _get_poses(batch_size):
        result = {
            "t": get_t(batch_size),
            "standing": get_standing(batch_size),
            "sitting": get_sitdown(batch_size),
            "curve": get_curve(batch_size),
            "hands-on": get_hands_on(batch_size),
        }
        return result

