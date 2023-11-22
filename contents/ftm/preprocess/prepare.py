import copy
import os
import pickle

import numpy as np
import torch
import open3d as o3d

from contents.ftm.model import FLAMESet
from contents.ftm.preprocess.convention import get_coordinates, get_names, get_circ_coordinates
from utilities.convention import ModelPath


def get_flame():
    root = r"D:\Creadto\Utilities\Dataset-maker\contents\external\flame"
    generic_path = ModelPath(root=root,
                             filename="generic_model.pkl",
                             config=os.path.join(root, "flame.yaml")
                             )
    flame = FLAMESet(generic_path, gender=True)
    return flame


def make_origin():
    flame = get_flame()
    shape = torch.zeros(2, 300)
    expression = torch.zeros(2, 100)

    v, lndmrks = flame(genders=['male', 'female'], batch_size=2, shape=shape, expression=expression)
    face = flame.faces
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(v[0])
    mesh.triangles = o3d.utility.Vector3iVector(face)
    o3d.io.write_triangle_mesh('origin.obj', mesh)


def make_obj_mapper():
    flame = get_flame()
    shape = torch.zeros(1, 300)
    expression = torch.zeros(1, 100)
    offset = torch.zeros(1, 3).type(torch.DoubleTensor)
    v, _ = flame(genders=['male'], batch_size=1, shape=shape, expression=expression, translation=offset)
    face = flame.faces

    dump = o3d.geometry.TriangleMesh()
    dump.vertices = o3d.utility.Vector3dVector(v[0])
    dump.triangles = o3d.utility.Vector3iVector(face)
    o3d.io.write_triangle_mesh('dump.obj', dump)
    dump = o3d.io.read_triangle_mesh('dump.obj')

    v2 = np.asarray(dump.vertices)

    mapper = []
    # error 비교
    for xyz in v2:
        x, y, z = xyz
        target = copy.deepcopy(v[0])
        target[:, 0] = abs(target[:, 0] - x)
        target[:, 1] = abs(target[:, 1] - y)
        target[:, 2] = abs(target[:, 2] - z)
        result = torch.sum(target, dim=1)
        index = torch.argmin(result)
        print(result.min())
        mapper.append(index.item())

    with open('mapper.pickle', 'wb') as f:
        pickle.dump(mapper, f)


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


def make_index_list(vertices, coordinates, name_dict: dict, error_display=False, verbose=False):
    flame = get_flame()
    with open(file='./mapper.pickle', mode='rb') as f:
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
            shape = (torch.rand(1, 300) - 0.5)
            expression = torch.zeros(1, 100)
            offset = torch.zeros(1, 3)
            offset[0, 0] = 1.0
            pick = np.random.choice(['male', 'female'], 1)
            v, _ = flame(genders=[pick.item()], batch_size=1, shape=shape, expression=expression, translation=offset)

            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(v[0])
            colors = np.zeros((len(v[0]), 3))
            colors += 0.4
            colors[mapper[index.item()], 0] = 1.0
            pcd.colors = o3d.utility.Vector3dVector(colors)
            o3d.visualization.draw_geometries([pcd])

    return name_dict


def make_circ_json(vertices, error_display=False, verbose=False):
    flame = get_flame()
    with open(file='./mapper.pickle', mode='rb') as f:
        mapper = pickle.load(f)
    circ_dict = get_circ_coordinates()
    json_dict = dict()
    for key, value in circ_dict.items():
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
            shape = (torch.rand(1, 300) - 0.5)
            expression = torch.zeros(1, 100)
            offset = torch.zeros(1, 3)
            pick = np.random.choice(['male', 'female'], 1)
            v, _ = flame(genders=[pick.item()], batch_size=1, shape=shape, expression=expression, translation=offset)
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


def run():
    mesh = o3d.io.read_triangle_mesh("../data/origin.obj")

    make_obj_mapper()
    coordinates = get_coordinates()
    names = get_names()

    check_error(np.asarray(mesh.vertices), coordinates)

    result = make_index_list(np.asarray(mesh.vertices), coordinates, names, True, False)
    circ_dict = make_circ_json(np.asarray(mesh.vertices), True, False)
    import json

    with open('facial.json', 'w', encoding='UTF-8-sig') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    with open('circumference-facial.json', 'w', encoding='UTF-8-sig') as f:
        json.dump(circ_dict, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    run()
