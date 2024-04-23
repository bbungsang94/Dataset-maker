import os
import copy
import pickle

import numpy as np
import open3d as o3d
import torch

from contents.stm.postprocess.merge_head import get_orient_coordinates
from contents.stm.preprocess.convention import get_coordinates, get_names, get_circ_coordinates
from contents.stm.model import SMPL
from contents.stm.poses.pose import get_t, get_hands_on, get_sitdown, get_curve, get_standing


def check_error(vertices, coordinates):
    indexes = []
    for alter in coordinates:
        x, z, y = alter
        target = copy.deepcopy(vertices)
        target[:, 0] = abs(target[:, 0] - x)
        target[:, 1] = abs(target[:, 1] - y)
        target[:, 2] = abs(target[:, 2] + z)
        result = np.sum(target, axis=1)
        index = np.argmin(result)
        indexes.append(index)
        print(result.min())


def make_origin(gender: str):
    root = r"D:\Creadto\Utilities\Dataset-maker\contents\external\smpl"
    model = SMPL(os.path.join(root, "SMPLX_" + gender.upper() + ".pkl"))
    shape = torch.zeros(1, 400, dtype=torch.float64)
    poses = {
        't': get_t(1),
        'hands-on': get_hands_on(1),
        'standing': get_standing(1),
        'curve': get_curve(1),
        'sitting': get_sitdown(1)
    }
    offset = torch.zeros(1, 3, dtype=torch.float64)
    for key, pose in poses.items():
        v, _ = model(shape, pose, offset)

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(v[0])
        mesh.triangles = o3d.utility.Vector3iVector(model.faces)
        o3d.io.write_triangle_mesh(key + '-origin.obj', mesh)
    
def make_obj_mapper():
    root = r"D:\Creadto\Utilities\Dataset-maker\contents\external\smpl"
    male = SMPL(os.path.join(root, "SMPLX_MALE.pkl"))

    shape = (torch.rand(1, 400) - 0.5).type(torch.DoubleTensor)
    pose = get_t(1)
    offset = torch.zeros(1, 3).type(torch.DoubleTensor)
    v1, _ = male(shape, pose, offset)

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(v1[0])
    mesh.triangles = o3d.utility.Vector3iVector(male.faces)
    o3d.io.write_triangle_mesh('dump.obj', mesh)
    pcd = o3d.io.read_triangle_mesh('dump.obj')

    v2 = np.asarray(pcd.vertices)

    mapper = []
    # error 비교
    for xyz in v2:
        x, y, z = xyz
        target = copy.deepcopy(v1[0])
        target[:, 0] = abs(target[:, 0] - x)
        target[:, 1] = abs(target[:, 1] - y)
        target[:, 2] = abs(target[:, 2] - z)
        result = torch.sum(target, dim=1)
        index = torch.argmin(result)
        print(result.min())
        mapper.append(index.item())

    with open('mapper.pickle', 'wb') as f:
        pickle.dump(mapper, f)


def make_index_list(vertices, coordinates, name_dict: dict, error_display=False, verbose=False):
    root = r"D:\Creadto\Utilities\Dataset-maker\contents\external\smpl"
    female = SMPL(os.path.join(root, "SMPLX_FEMALE.pkl"))
    male = SMPL(os.path.join(root, "SMPLX_MALE.pkl"))
    model = [male, female]
    poses = [get_t, get_hands_on, get_sitdown, get_curve, get_standing]
    with open(file='../data/mapper.pickle', mode='rb') as f:
        mapper = pickle.load(f)

    for idx, key in enumerate(name_dict.keys()):
        x, z, y = coordinates[idx]
        target = copy.deepcopy(vertices)
        target[:, 0] = abs(target[:, 0] - x)
        target[:, 1] = abs(target[:, 1] - y)
        target[:, 2] = abs(target[:, 2] + z)
        result = np.sum(target, axis=1)
        index = np.argmin(result)
        value = result[index]
        name_dict[key] = mapper[index.item()]
        if error_display:
            print("Tag: " + key + " Index: %05d Error: %.8f" % (mapper[index.item()], value))
        if verbose:
            shape = (torch.rand(1, 400) - 0.5).type(torch.DoubleTensor)
            pose = poses[np.random.randint(0, 5)](1)
            offset = torch.zeros(1, 3).type(torch.DoubleTensor)
            offset[0, 0] = 1.0
            pick = np.random.randint(0, 2)
            v, _ = model[pick](shape, pose, offset)

            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(v[0])
            colors = np.zeros((len(v[0]), 3))
            colors += 0.4
            colors[mapper[index.item()], 0] = 1.0
            pcd.colors = o3d.utility.Vector3dVector(colors)
            o3d.visualization.draw_geometries([pcd])

    return name_dict


def make_circ_json(vertices, target_points, error_display=False, verbose=False):
    root = r"D:\Creadto\Utilities\Dataset-maker\contents\external\smpl"
    female = SMPL(os.path.join(root, "SMPLX_FEMALE.pkl"))
    male = SMPL(os.path.join(root, "SMPLX_MALE.pkl"))
    model = [male, female]
    poses = [get_t, get_hands_on, get_sitdown, get_curve, get_standing]
    with open(file='../data/mapper.pickle', mode='rb') as f:
        mapper = pickle.load(f)
    json_dict = dict()
    for key, value in target_points.items():
        json_dict[key] = []
        print(key)
        for xyz in value:
            x, z, y = xyz
            target = copy.deepcopy(vertices)
            target[:, 0] = abs(target[:, 0] - x)
            target[:, 1] = abs(target[:, 1] - y)
            target[:, 2] = abs(target[:, 2] + z)
            result = np.sum(target, axis=1)
            index = np.argmin(result)
            value = result[index]
            json_dict[key].append(mapper[index.item()])
            if error_display:
                print("Error: %.8f" % value)

        if verbose:
            points = []
            lines = []
            shape = (torch.rand(1, 400) - 0.5).type(torch.DoubleTensor)
            pose = poses[np.random.randint(0, 5)](1)
            offset = torch.zeros(1, 3).type(torch.DoubleTensor)
            pick = np.random.randint(0, 2)
            v, _ = model[pick](shape, pose, offset)
            colors = np.zeros((len(v[0]), 3))
            colors += 0.4
            for count, index in enumerate(json_dict[key]):
                colors[index, 0] = 1.0
                lines.append([count, (count+1) % len(json_dict[key])])
                points.append(v[0][index].numpy())

            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(v[0])
            pcd.colors = o3d.utility.Vector3dVector(colors)
            line = o3d.geometry.LineSet()
            line.points = o3d.utility.Vector3dVector(np.array(points))
            line.lines = o3d.utility.Vector2iVector(np.array(lines))
            colors = np.zeros((len(v[0]), 3))
            colors[:, 1] = 1.0
            line.colors = o3d.utility.Vector3dVector(colors)
            o3d.visualization.draw_geometries([pcd, line])
    return json_dict


if __name__ == "__main__":
    # make_origin("female")
    mesh = o3d.io.read_triangle_mesh(os.path.join(r"../poses/sizekorea", "origin-male.obj"))
    # coordi = o3d.geometry.TriangleMesh.create_coordinate_frame()
    # o3d.visualization.draw_geometries([mesh, coordi])
    # #make_obj_mapper()
    standing_coordinates, sitting_coordinates = get_coordinates()
    # neck = get_orient_coordinates()
    standing_names, sitting_names = get_names()

    check_error(np.asarray(mesh.vertices), standing_coordinates)
    check_error(np.asarray(mesh.vertices), sitting_coordinates)

    standing_names = make_index_list(np.asarray(mesh.vertices), standing_coordinates, standing_names, True, False)
    sitting_names = make_index_list(np.asarray(mesh.vertices), sitting_coordinates, sitting_names, True, False)
    circ_result = make_circ_json(np.asarray(mesh.vertices), get_circ_coordinates(), True, False)
    # neck_oriented = make_circ_json(np.asarray(mesh.vertices), get_orient_coordinates(), True, False)
    import json

    with open('standing.json', 'w', encoding='UTF-8-sig') as f:
        json.dump(standing_names, f, indent=4, ensure_ascii=False)
    with open('sitting.json', 'w', encoding='UTF-8-sig') as f:
        json.dump(sitting_names, f, indent=4, ensure_ascii=False)
    with open('circumference.json', 'w', encoding='UTF-8-sig') as f:
        json.dump(circ_result, f, indent=4, ensure_ascii=False)
    # with open('neck_oriented.json', 'w', encoding='UTF-8-sig') as f:
    #     json.dump(neck_oriented, f, indent=4, ensure_ascii=False)
