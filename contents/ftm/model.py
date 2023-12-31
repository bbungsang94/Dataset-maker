import os
import pickle
import argparse
from typing import Dict, Any

import numpy as np
import torch
import torch.nn as nn
from smplx.lbs import batch_rodrigues, lbs, vertices2landmarks
from smplx.utils import Struct, rot_mat_to_euler, to_np, to_tensor
import open3d as o3d

from utilities.convention import ModelPath


class FLAMESet(nn.Module):
    def __init__(self, arg: ModelPath, gender: bool, **kwargs):
        super().__init__()
        arg.config['static_landmark_embedding_path'] = os.path.join(arg.root,
                                                                    arg.config['static_landmark_embedding_path'])
        arg.config['dynamic_landmark_embedding_path'] = os.path.join(arg.root,
                                                                     arg.config['dynamic_landmark_embedding_path'])

        if gender:
            male_path = arg.full_path.replace('generic', 'male')
            male = FLAME(flame_model_path=male_path, **arg.config)
            female_path = arg.full_path.replace('generic', 'female')
            female = FLAME(flame_model_path=female_path, **arg.config)
            self.model = nn.ModuleDict({'male': male, 'female': female})
        else:
            generic = FLAME(flame_model_path=arg.full_path, **arg.config)
            self.model = nn.ModuleDict({'generic': generic})

    @property
    def faces(self):
        for value in self.model.values():
            return value.faces

    def forward(self, genders, **kwargs):
        vertices, landmarks = torch.zeros(len(genders), 5023, 3), torch.zeros(len(genders), 51, 3)
        for i, gender in enumerate(genders):
            vx, lnk = self.model[gender](**kwargs)
            vertices[i], landmarks[i] = vx[i], lnk[i]
        return vertices, landmarks


class FLAME(nn.Module):
    """
    Given flame parameters this class generates a differentiable FLAME function
    which outputs the a mesh and 3D facial landmarks
    """

    def __init__(self, flame_model_path, static_landmark_embedding_path, dynamic_landmark_embedding_path,
                 use_face_contour, constants):
        super(FLAME, self).__init__()
        with open(flame_model_path, "rb") as f:
            model_info = pickle.load(f, encoding="latin1")
            model = o3d.geometry.TriangleMesh()
            model.vertices = o3d.utility.Vector3dVector(model_info['v_template'])
            model.triangles = o3d.utility.Vector3iVector(model_info['f'])

            stub = flame_model_path.split('\\')
            # o3d.io.write_triangle_mesh(stub[-1].replace('pkl', 'obj'), model)
            self.flame_model = Struct(**model_info)

        self.NECK_IDX = 1
        self.dtype = torch.float32
        self.use_face_contour = use_face_contour
        self.faces = self.flame_model.f
        self.constants = constants
        self.register_buffer("faces_tensor", to_tensor(to_np(self.faces, dtype=np.int64), dtype=torch.long))

        # Fixing remaining Shape betas
        # There are total 300 shape parameters to control FLAME; But one can use the first few parameters to express
        # the shape. For example 100 shape parameters are used for RingNet project
        default_shape = torch.zeros(
            [1, 300 - constants['shape']],
            dtype=self.dtype,
            requires_grad=False,
        )
        self.register_parameter(
            "shape_betas", nn.Parameter(default_shape, requires_grad=False)
        )

        # Fixing remaining expression betas
        # There are total 100 shape expression parameters to control FLAME; But one can use the first few parameters to express
        # the expression. For example 50 expression parameters are used for RingNet project
        default_exp = torch.zeros([1, 100 - constants['expression']],
                                  dtype=self.dtype, requires_grad=False)
        self.register_parameter("expression_betas", nn.Parameter(default_exp, requires_grad=False))

        default_rot = torch.zeros([1, 3], dtype=self.dtype, requires_grad=False)
        self.register_parameter("rot", nn.Parameter(default_rot, requires_grad=False))

        default_jaw = torch.zeros([1, 3], dtype=self.dtype, requires_grad=False)
        self.register_parameter("jaw", nn.Parameter(default_jaw, requires_grad=False))

        # Eyeball and neck rotation
        default_eyball_pose = torch.zeros([1, 6], dtype=self.dtype, requires_grad=False)
        self.register_parameter("eye_pose", nn.Parameter(default_eyball_pose, requires_grad=False))

        default_neck_pose = torch.zeros([1, 3], dtype=self.dtype, requires_grad=False)
        self.register_parameter("neck_pose", nn.Parameter(default_neck_pose, requires_grad=False))

        # default_transl = torch.zeros([self.batch_size, 3], dtype=self.dtype, requires_grad=False)
        # self.register_parameter("transl", nn.Parameter(default_transl, requires_grad=False))

        # The vertices of the template model
        self.register_buffer("v_template", to_tensor(to_np(self.flame_model.v_template), dtype=self.dtype))

        # The shape components
        shapedirs = self.flame_model.shapedirs
        # The shape components
        self.register_buffer("shapedirs", to_tensor(to_np(shapedirs), dtype=self.dtype))

        j_regressor = to_tensor(to_np(self.flame_model.J_regressor), dtype=self.dtype)
        self.register_buffer("J_regressor", j_regressor)

        # Pose blend shape basis
        num_pose_basis = self.flame_model.posedirs.shape[-1]
        posedirs = np.reshape(self.flame_model.posedirs, [-1, num_pose_basis]).T
        self.register_buffer("posedirs", to_tensor(to_np(posedirs), dtype=self.dtype))

        # indices of parents for each joints
        parents = to_tensor(to_np(self.flame_model.kintree_table[0])).long()
        parents[0] = -1
        self.register_buffer("parents", parents)

        self.register_buffer("lbs_weights", to_tensor(to_np(self.flame_model.weights), dtype=self.dtype))

        # Static and Dynamic Landmark embeddings for FLAME

        with open(static_landmark_embedding_path, "rb") as f:
            static_embeddings = Struct(**pickle.load(f, encoding="latin1"))

        lmk_faces_idx = (static_embeddings.lmk_face_idx).astype(np.int64)
        self.register_buffer("lmk_faces_idx", torch.tensor(lmk_faces_idx, dtype=torch.long))
        lmk_bary_coords = static_embeddings.lmk_b_coords
        self.register_buffer("lmk_bary_coords", torch.tensor(lmk_bary_coords, dtype=self.dtype))

        if self.use_face_contour:
            conture_embeddings = np.load(dynamic_landmark_embedding_path, allow_pickle=True, encoding="latin1")
            conture_embeddings = conture_embeddings[()]
            dynamic_lmk_faces_idx = np.array(conture_embeddings["lmk_face_idx"]).astype(np.int64)
            dynamic_lmk_faces_idx = torch.tensor(dynamic_lmk_faces_idx, dtype=torch.long)
            self.register_buffer("dynamic_lmk_faces_idx", dynamic_lmk_faces_idx)

            dynamic_lmk_bary_coords = conture_embeddings["lmk_b_coords"]
            dynamic_lmk_bary_coords = np.array(dynamic_lmk_bary_coords)
            dynamic_lmk_bary_coords = torch.tensor(dynamic_lmk_bary_coords, dtype=self.dtype)
            self.register_buffer("dynamic_lmk_bary_coords", dynamic_lmk_bary_coords)

            neck_kin_chain = []
            curr_idx = torch.tensor(self.NECK_IDX, dtype=torch.long)
            while curr_idx != -1:
                neck_kin_chain.append(curr_idx)
                curr_idx = self.parents[curr_idx]
            self.register_buffer("neck_kin_chain", torch.stack(neck_kin_chain))

    def _find_dynamic_lmk_idx_and_bcoords(
            self,
            vertices,
            pose,
            dynamic_lmk_faces_idx,
            dynamic_lmk_b_coords,
            neck_kin_chain,
            dtype=torch.float32,
    ):
        """
        Selects the face contour depending on the reletive position of the head
        Input:
            vertices: N X num_of_vertices X 3
            pose: N X full pose
            dynamic_lmk_faces_idx: The list of contour face indexes
            dynamic_lmk_b_coords: The list of contour barycentric weights
            neck_kin_chain: The tree to consider for the relative rotation
            dtype: Data type
        return:
            The contour face indexes and the corresponding barycentric weights
        Source: Modified for batches from https://github.com/vchoutas/smplx
        """

        batch_size = vertices.shape[0]

        aa_pose = torch.index_select(pose.view(batch_size, -1, 3), 1, neck_kin_chain)
        rot_mats = batch_rodrigues(aa_pose.view(-1, 3)).view(batch_size, -1, 3, 3)

        rel_rot_mat = (
            torch.eye(3, device=vertices.device, dtype=dtype)
            .unsqueeze_(dim=0)
            .expand(batch_size, -1, -1)
        )
        for idx in range(len(neck_kin_chain)):
            rel_rot_mat = torch.bmm(rot_mats[:, idx], rel_rot_mat)

        y_rot_angle = torch.round(
            torch.clamp(-rot_mat_to_euler(rel_rot_mat) * 180.0 / np.pi, max=39)
        ).to(dtype=torch.long)
        neg_mask = y_rot_angle.lt(0).to(dtype=torch.long)
        mask = y_rot_angle.lt(-39).to(dtype=torch.long)
        neg_vals = mask * 78 + (1 - mask) * (39 - y_rot_angle)
        y_rot_angle = neg_mask * neg_vals + (1 - neg_mask) * y_rot_angle

        dyn_lmk_faces_idx = torch.index_select(dynamic_lmk_faces_idx, 0, y_rot_angle)
        dyn_lmk_b_coords = torch.index_select(dynamic_lmk_b_coords, 0, y_rot_angle)

        return dyn_lmk_faces_idx, dyn_lmk_b_coords

    def forward(
            self,
            batch_size=1,
            shape=None,
            expression=None,
            rotation=None,
            translation=None,
            scale=None,
            jaw=None,
            eyeballs=None,
            neck=None,
    ):
        """
        Input:
            shape_params: N X number of shape parameters
            expression_params: N X number of expression parameters
            pose_params: N X number of pose parameters
        return:
            vertices: N X V X 3
            landmarks: N X number of landmarks X 3
        """

        betas = torch.cat(
            [
                shape,
                self.shape_betas[[0]].expand(batch_size, -1),
                expression,
                self.expression_betas[[0]].expand(batch_size, -1)
            ],
            dim=1,
        )
        neck_pose = neck if neck is not None else self.neck_pose[[0]].expand(batch_size, -1)
        eye_pose = eyeballs if eyeballs is not None else self.eye_pose[[0]].expand(batch_size, -1)
        rotation_params = rotation if rotation is not None else self.rot[[0]].expand(batch_size, -1)
        jaw = jaw if jaw is not None else self.jaw[[0]].expand(batch_size, -1)
        # full_pose = torch.cat(
        #     [rotation_params, neck_pose, jaw, eye_pose], dim=1
        # )
        full_pose = torch.cat(
            [neck_pose, neck_pose, jaw, eye_pose], dim=1
        )
        template_vertices = self.v_template.unsqueeze(0).repeat(batch_size, 1, 1)

        vertices, _ = lbs(
            betas,
            full_pose,
            template_vertices,
            self.shapedirs,
            self.posedirs,
            self.J_regressor,
            self.parents,
            self.lbs_weights,
        )

        lmk_faces_idx = self.lmk_faces_idx.unsqueeze(dim=0).repeat(batch_size, 1)
        lmk_bary_coords = self.lmk_bary_coords.unsqueeze(dim=0).repeat(
            batch_size, 1, 1
        )

        landmarks = vertices2landmarks(
            vertices, self.faces_tensor, lmk_faces_idx, lmk_bary_coords
        )

        return vertices, landmarks
