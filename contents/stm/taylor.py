import numpy as np
import open3d as o3d


class Taylor:
    def __init__(self, tape, pin, model_dict=None):
        """
        :param tape: It's interaction list from convention.py. call get_interactions
        :param pin: Vertices index about human parts in 3d mesh model load standing/sitting.json
        """
        self.tape = tape
        self.pin = self._convert_tag(pin)
        self.table = np.zeros(len(self.tape))
        self.model = model_dict

    def update(self, model_dict):
        """
        :param model_dict: vertices ("standing", "sitting", "t", "hands-on", "curve")
        :return:
        """
        self.model = model_dict
        self.table = np.zeros(len(self.tape))

    def order(self, fast=False, visualize=False):
        for i, paper in enumerate(self.tape):
            kor, eng, tags, func, pose = paper
            # points name to index
            args = []
            for tag in tags:
                index = self.pin[tag]
                if visualize:
                    print(tag)
                    pcd = o3d.geometry.PointCloud()
                    pcd.points = o3d.utility.Vector3dVector(self.model[pose][0].numpy())
                    colors = np.zeros((len(self.model[pose][0]), 3))
                    colors[index, 0] = 1.0
                    pcd.colors = o3d.utility.Vector3dVector(colors)
                    o3d.visualization.draw_geometries([pcd])

                point = self.model[pose][0, index]
                args.append(point)

            # function 인식
            if fast and ("circ" in func or "length" in func):
                continue
            if "circ" in func:
                stub = func.split('-')
                args.insert(0, stub[-1])
                      
            value = getattr(self, func)(*args)
            
            if visualize:
                # 이거 반드시 봐야함
                pass
            
            self.table[i] = value
        return self.table

    def _convert_tag(self, pin):
        standing, sitting = pin
        tag = dict()
        for key, value in standing.items():
            _, eng, direction = self._separate_key(key)
            tag[eng + direction] = value

        for key, value in sitting.items():
            _, eng, direction = self._separate_key(key)
            tag[eng + direction] = value
        return tag

    @staticmethod
    def _separate_key(name):
        stub = name.split(', ')
        if len(stub[-1]) > 1:
            direction = ""
        else:
            direction = ", " + stub[-1]
        return stub[0], stub[1], direction

    @staticmethod
    def width(a, b):
        return abs(a[0] - b[0])

    @staticmethod
    def height(a, b):
        return abs(a[1] - b[1])

    @staticmethod
    def depth(a, b):
        return abs(a[2] - b[2])

    @staticmethod
    def circ(direction, *args):
        return -1

    @staticmethod
    def length(*args):
        return -1


