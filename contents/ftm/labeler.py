import copy
import json
import os

import numpy as np
import torch

from contents.ftm.model import FLAMESet
from contents.ftm.preprocess.convention import get_interactions
from contents.stm.tailor import GraphTailor
from labeler.torchbase import Base
from utilities.convention import ModelPath


class GraphLabeler(Base):
    def __init__(self, flame_root, pin_root, circ_root):
        self.batch_size = 1
        self.count = 0

        generic_path = ModelPath(root=flame_root,
                                 filename="generic_model.pkl",
                                 config=os.path.join(flame_root, "flame.yaml")
                                 )

        with open(os.path.join(pin_root, 'facial.json'), 'r', encoding='UTF-8-sig') as f:
            facial = json.load(f)
        with open(os.path.join(circ_root, 'circumference-facial.json'), 'r', encoding='UTF-8-sig') as f:
            circ_dict = json.load(f)

        self.model = FLAMESet(generic_path, gender=True)
        self.tailor = GraphTailor(tape=get_interactions(), pin=[facial], circ_dict=circ_dict)

    def __call__(self, **kwargs):
        shape = kwargs['value'].type(torch.FloatTensor)
        gender = np.random.choice(['male', 'female'], 1).item()

        poses = self._get_poses(batch_size=self.batch_size)
        models = dict()
        for key, value in poses.items():
            v, _ = self.model(genders=[gender], batch_size=1, shape=shape, expression=value)
            models[key] = copy.deepcopy(v)

        self.tailor.update(model_dict=models)
        measure, graph = self.tailor.get_measured_graph(gender=[gender], fast=False, visualize=False)
        result = {
            'input': {
                'gender': gender,
                'shape': shape
            },
            'output': {
                'graph': graph[0],
                'measure': measure
            }
        }
        self.save(result, os.path.join(kwargs['output_path'], "%06d.pth" % self.count))
        self.count += 1

        return None

    @staticmethod
    def _get_poses(batch_size):
        result = {
            "standard": torch.zeros(batch_size, 100),
        }
        return result
