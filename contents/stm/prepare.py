import os
import copy
import numpy as np
import open3d as o3d

from contents.stm.convention import get_coordinates, get_names


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


def make_index_list(vertices, coordinates, name_dict: dict):
    for idx, key in enumerate(name_dict.keys()):
        x, z, y = coordinates[idx]
        target = copy.deepcopy(vertices)
        target[:, 0] = abs(target[:, 0] - x)
        target[:, 1] = abs(target[:, 1] - y)
        target[:, 2] = abs(target[:, 2] + z)
        result = np.sum(target, axis=1)
        index = np.argmin(result)
        name_dict[key] = index.item()
    return name_dict


if __name__ == "__main__":
    mesh = o3d.io.read_triangle_mesh(os.path.join(r"D:\Creadto\Utilities\Dataset-maker\contents\stm\165poses\sizekorea",
                                                  "origin-male.obj"))
    # coordi = o3d.geometry.TriangleMesh.create_coordinate_frame()
    # o3d.visualization.draw_geometries([mesh, coordi])
    standing_coordinates, sitting_coordinates = get_coordinates()
    standing_names, sitting_names = get_names()

    check_error(np.asarray(mesh.vertices), standing_coordinates)
    check_error(np.asarray(mesh.vertices), sitting_coordinates)

    standing_names = make_index_list(np.asarray(mesh.vertices), standing_coordinates, standing_names)
    sitting_names = make_index_list(np.asarray(mesh.vertices), sitting_coordinates, sitting_names)
    import json

    with open('standing.json', 'w', encoding='UTF-8-sig') as f:
        json.dump(standing_names, f, indent=4, ensure_ascii=False)
    with open('sitting.json', 'w', encoding='UTF-8-sig') as f:
        json.dump(sitting_names, f, indent=4, ensure_ascii=False)
