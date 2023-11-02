import numpy as np
import torch
import copy
import open3d as o3d

from contents.stm.model import SMPLSet


def get_t(batch_size):
    p = np.zeros((batch_size, 55, 3))

    return torch.from_numpy(p.reshape((batch_size, -1)))


def get_hands_on(batch_size):
    p = np.zeros((batch_size, 55, 3))

    p[:, 13, 2] = 0.5
    p[:, 14, 2] = -0.5
    p[:, 16, 2] = 1.0
    p[:, 17, 2] = -1.0
    #
    p[:, 18, 0] = -0.5
    p[:, 19, 0] = -0.5
    p[:, 20, 0] = -1.0
    p[:, 21, 0] = -1.0

    return torch.from_numpy(p.reshape((batch_size, -1)))


def get_standing(batch_size):
    p = np.zeros((batch_size, 55, 3))

    p[:, 13, 0] = -0.2
    p[:, 14, 0] = -0.2
    p[:, 13, 2] = -0.4
    p[:, 14, 2] = 0.4
    p[:, 16, 2] = -1.0
    p[:, 17, 2] = 1.0
    return torch.from_numpy(p.reshape((batch_size, -1)))


def get_curve(batch_size):
    p = np.zeros((batch_size, 55, 3))
    # p[:, 1, 0] = -1.5
    # p[:, 2, 0] = -1.5
    # p[:, 4, 0] = 1.5
    # p[:, 5, 0] = 1.5

    p[:, 13, 2] = -0.5
    p[:, 14, 2] = 0.5
    p[:, 16, 2] = -0.75
    p[:, 17, 2] = 0.75

    p[:, 18, 1] = -1.5
    p[:, 19, 1] = 1.5
    return torch.from_numpy(p.reshape((batch_size, -1)))


def get_sitdown(batch_size):
    p = np.zeros((batch_size, 55, 3))
    p[:, 1, 0] = -1.5
    p[:, 2, 0] = -1.5
    p[:, 4, 0] = 1.5
    p[:, 5, 0] = 1.5

    p[:, 13, 2] = -0.5
    p[:, 14, 2] = 0.5
    p[:, 16, 2] = -0.75
    p[:, 17, 2] = 0.75

    p[:, 18, 1] = -1.5
    p[:, 19, 1] = 1.5
    return torch.from_numpy(p.reshape((batch_size, -1)))


def make_t(filename):
    model = SMPLSet('../../external/smpl/SMPLX_NEUTRAL.pkl')
    fcs = model.faces
    batch_size = 3
    g = ['male', 'female', 'neutral']
    b = np.zeros((batch_size, 400))
    b = np.random.rand(batch_size, 400) * - 0.5
    p = np.zeros((batch_size, 55, 3))
    of = np.zeros((batch_size, 3))

    p = p.reshape((batch_size, -1))
    re = model(genders=g, beta=torch.from_numpy(b), pose=torch.from_numpy(p), offset=torch.from_numpy(of))
    for i, v in enumerate(re):
        v = np.array(v)
        mesh = o3d.geometry.TriangleMesh()
        mesh.triangles = o3d.utility.Vector3iVector(fcs[g[i]])
        mesh.vertices = o3d.utility.Vector3dVector(v)
        o3d.io.write_triangle_mesh(filename=filename.replace('t', g[i] + '-t'), mesh=mesh)


def make_hands_on(filename):
    model = SMPLSet('../../external/smpl/SMPLX_NEUTRAL.pkl')
    fcs = model.faces
    batch_size = 3
    g = ['male', 'female', 'neutral']
    b = np.zeros((batch_size, 400))
    b = np.random.rand(batch_size, 400) * - 0.5
    p = np.zeros((batch_size, 55, 3))
    of = np.zeros((batch_size, 3))

    p[:, 13, 2] = 0.5
    p[:, 14, 2] = -0.5
    p[:, 16, 2] = 1.0
    p[:, 17, 2] = -1.0
    #
    p[:, 18, 0] = -0.5
    p[:, 19, 0] = -0.5
    p[:, 20, 0] = -1.0
    p[:, 21, 0] = -1.0

    p = p.reshape((batch_size, -1))
    re = model(genders=g, beta=torch.from_numpy(b), pose=torch.from_numpy(p), offset=torch.from_numpy(of))
    for i, v in enumerate(re):
        v = np.array(v)
        mesh = o3d.geometry.TriangleMesh()
        mesh.triangles = o3d.utility.Vector3iVector(fcs[g[i]])
        mesh.vertices = o3d.utility.Vector3dVector(v)
        o3d.io.write_triangle_mesh(filename=filename.replace('handson', g[i] + '-handson'), mesh=mesh)


def make_ready(filename):
    model = SMPLSet('../../external/smpl/SMPLX_NEUTRAL.pkl')
    fcs = model.faces
    batch_size = 3
    g = ['male', 'female', 'neutral']
    b = np.zeros((batch_size, 400))
    b = np.random.rand(batch_size, 400) * - 0.5
    p = np.zeros((batch_size, 55, 3))
    of = np.zeros((batch_size, 3))

    p[:, 13, 0] = -0.2
    p[:, 14, 0] = -0.2
    p[:, 13, 2] = -0.4
    p[:, 14, 2] = 0.4
    p[:, 16, 2] = -1.0
    p[:, 17, 2] = 1.0
    p = p.reshape((batch_size, -1))
    re = model(genders=g, beta=torch.from_numpy(b), pose=torch.from_numpy(p), offset=torch.from_numpy(of))
    for i, v in enumerate(re):
        v = np.array(v)
        mesh = o3d.geometry.TriangleMesh()
        mesh.triangles = o3d.utility.Vector3iVector(fcs[g[i]])
        mesh.vertices = o3d.utility.Vector3dVector(v)
        o3d.io.write_triangle_mesh(filename=filename.replace('ready', g[i] + '-ready'), mesh=mesh)


def make_curve(filename):
    model = SMPLSet('../../external/smpl/SMPLX_NEUTRAL.pkl')
    fcs = model.faces
    batch_size = 3
    g = ['male', 'female', 'neutral']
    b = np.zeros((batch_size, 400))
    b = np.random.rand(batch_size, 400) * - 0.5
    p = np.zeros((batch_size, 55, 3))
    of = np.zeros((batch_size, 3))
    # p[:, 1, 0] = -1.5
    # p[:, 2, 0] = -1.5
    # p[:, 4, 0] = 1.5
    # p[:, 5, 0] = 1.5

    p[:, 13, 2] = -0.5
    p[:, 14, 2] = 0.5
    p[:, 16, 2] = -0.75
    p[:, 17, 2] = 0.75

    p[:, 18, 1] = -1.5
    p[:, 19, 1] = 1.5
    p = p.reshape((batch_size, -1))
    re = model(genders=g, beta=torch.from_numpy(b), pose=torch.from_numpy(p), offset=torch.from_numpy(of))
    for i, v in enumerate(re):
        v = np.array(v)
        mesh = o3d.geometry.TriangleMesh()
        mesh.triangles = o3d.utility.Vector3iVector(fcs[g[i]])
        mesh.vertices = o3d.utility.Vector3dVector(v)
        o3d.io.write_triangle_mesh(filename=filename.replace('train', g[i] + '-train'), mesh=mesh)


def make_sitdown(filename):
    model = SMPLSet('../../external/smpl/SMPLX_NEUTRAL.pkl')
    fcs = model.faces
    batch_size = 3
    g = ['male', 'female', 'neutral']
    b = np.zeros((batch_size, 400))
    b = np.random.rand(batch_size, 400) * - 0.5
    p = np.zeros((batch_size, 55, 3))
    of = np.zeros((batch_size, 3))
    p[:, 1, 0] = -1.5
    p[:, 2, 0] = -1.5
    p[:, 4, 0] = 1.5
    p[:, 5, 0] = 1.5

    p[:, 13, 2] = -0.5
    p[:, 14, 2] = 0.5
    p[:, 16, 2] = -0.75
    p[:, 17, 2] = 0.75

    p[:, 18, 1] = -1.5
    p[:, 19, 1] = 1.5
    p = p.reshape((batch_size, -1))
    re = model(genders=g, beta=torch.from_numpy(b), pose=torch.from_numpy(p), offset=torch.from_numpy(of))
    for i, v in enumerate(re):
        v = np.array(v)
        mesh = o3d.geometry.TriangleMesh()
        mesh.triangles = o3d.utility.Vector3iVector(fcs[g[i]])
        mesh.vertices = o3d.utility.Vector3dVector(v)
        o3d.io.write_triangle_mesh(filename=filename.replace('sitdown', g[i] + '-sitdown'), mesh=mesh)


def main():
    model = SMPLSet('../../external/smpl/SMPLX_NEUTRAL.pkl')
    fcs = model.faces
    batch_size = 3
    g = ['male', 'female', 'neutral']
    b = np.zeros((batch_size, 400))
    p = np.zeros((batch_size, 55, 3))
    of = np.zeros((batch_size, 3))
    for itr in range(55):
        du = copy.deepcopy(p)
        du[:, itr, :] = 0.2
        du = du.reshape((batch_size, -1))
        re = model(genders=g, beta=torch.from_numpy(b), pose=torch.from_numpy(du), offset=torch.from_numpy(of))
        for i, v in enumerate(re):
            v = np.array(v)
            mesh = o3d.geometry.TriangleMesh()
            mesh.triangles = o3d.utility.Vector3iVector(fcs[g[i]])
            mesh.vertices = o3d.utility.Vector3dVector(v)
            filename = "./pos/" + g[i] + "%02d" % itr + "positive.obj"
            o3d.io.write_triangle_mesh(filename=filename, mesh=mesh)


if __name__ == "__main__":
    # main()
    # make_ready(filename="./sizekorea/ready.obj")
    # make_sitdown(filename="./sizekorea/sitdown.obj")
    # make_hands_on(filename="./sizekorea/handson.obj")
    make_t(filename="./sizekorea/t.obj")
