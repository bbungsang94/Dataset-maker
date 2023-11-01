import copy
import json
import os
import pickle
from typing import List

import pandas as pd
import torch
import torch.nn as nn

from contents.stm.utilities import rodrigues, with_zeros, pack


class Maker:
    def __init__(self, structure_root, data_root):
        with open(os.path.join(structure_root, "sitting.json"), 'r') as f:
            self.sitting = json.load(f)
        with open(os.path.join(structure_root, "standing.json"), 'r') as f:
            self.standing = json.load(f)
        data = pd.read_csv(os.path.join(data_root, "dataset.csv"), index_col="Index")


class SMPLSet(nn.Module):
    def __init__(self, path: str):
        super().__init__()

        male_path = path.replace("NEUTRAL", "MALE")
        female_path = path.replace("NEUTRAL", "FEMALE")
        male = SMPL(path=male_path)
        female = SMPL(path=female_path)
        neutral = SMPL(path=path)
        self.model = nn.ModuleDict({'male': male, 'female': female, 'neutral': neutral})

    @property
    def faces(self):
        faces = {}
        for key, value in self.model.items():
            faces[key] = value.faces
        return faces

    def forward(self, genders: List[str], beta: torch.Tensor, pose: torch.Tensor, offset: torch.Tensor):
        batches = []
        for i, gender in enumerate(genders):
            result, joint = self.model[gender](beta[i].unsqueeze(0), pose[i].unsqueeze(0), offset[i].unsqueeze(0))
            batches.append(copy.deepcopy(result))
        batches = torch.cat(batches)
        return batches


class SMPL(nn.Module):
    def __init__(self, path):
        super(SMPL, self).__init__()
        with open(path, 'rb') as f:
            source = pickle.load(f, encoding="latin1")
        self.joint_regressor = torch.from_numpy(source['J_regressor']).type(torch.float64)
        self.weights = torch.from_numpy(source['weights']).type(torch.float64)
        self.posedirs = torch.from_numpy(source['posedirs']).type(torch.float64)
        self.v_template = torch.from_numpy(source['v_template']).type(torch.float64)
        self.shapedirs = torch.from_numpy(source['shapedirs']).type(torch.float64)
        self.kintree_table = source['kintree_table']
        self.faces = source['f']
        self.device = torch.device('cpu')

    def to(self, device, *args, **kwargs):
        super(SMPL, self).to(device=device, *args, **kwargs)
        self.device = device

    def forward(self, beta, pose, offset):
        batch_num = beta.shape[0]
        id_to_col = {self.kintree_table[1, i]: i
                     for i in range(self.kintree_table.shape[1])}
        parent = {
            i: id_to_col[self.kintree_table[0, i]]
            for i in range(1, self.kintree_table.shape[1])
        }
        v_shaped = torch.tensordot(beta, self.shapedirs, dims=([1], [2])) + self.v_template
        joint = torch.matmul(self.joint_regressor, v_shaped)
        r_cube_big = rodrigues(pose.view(-1, 1, 3)).reshape(batch_num, -1, 3, 3)

        r_cube = r_cube_big[:, 1:, :, :]
        i_cube = (torch.eye(3, dtype=torch.float64).unsqueeze(dim=0) + torch.zeros((batch_num, r_cube.shape[1], 3, 3),
                                                                                   dtype=torch.float64)).to(self.device)
        lrotmin = (r_cube - i_cube).reshape(batch_num, -1, 1).squeeze(dim=2)
        v_posed = v_shaped + torch.tensordot(lrotmin, self.posedirs, dims=([1], [2]))

        results = []
        results.append(with_zeros(torch.cat((r_cube_big[:, 0], torch.reshape(joint[:, 0, :], (-1, 3, 1))), dim=2)))
        for i in range(1, self.kintree_table.shape[1]):
            results.append(torch.matmul(results[parent[i]], with_zeros(
                torch.cat((r_cube_big[:, i], torch.reshape(joint[:, i, :] - joint[:, parent[i], :], (-1, 3, 1))),
                          dim=2))))

        stacked = torch.stack(results, dim=1)
        results = stacked - pack(torch.matmul(stacked, torch.reshape(
            torch.cat((joint, torch.zeros((batch_num, 55, 1), dtype=torch.float64).to(self.device)), dim=2),
            (batch_num, 55, 4, 1))))
        # Restart from here
        T = torch.tensordot(results, self.weights, dims=([1], [1])).permute(0, 3, 1, 2)
        rest_shape_h = torch.cat(
            (v_posed, torch.ones((batch_num, v_posed.shape[1], 1), dtype=torch.float64).to(self.device)), dim=2
        )
        v = torch.matmul(T, torch.reshape(rest_shape_h, (batch_num, -1, 4, 1)))
        v = torch.reshape(v, (batch_num, -1, 4))[:, :, :3]
        result = v + torch.reshape(offset, (batch_num, 1, 3))
        # estimate 3D joint locations
        # print(result.shape)
        # print(self.joint_regressor.shape)
        joints = torch.tensordot(result, self.joint_regressor, dims=([1], [1])).transpose(1, 2)
        return result, joints
