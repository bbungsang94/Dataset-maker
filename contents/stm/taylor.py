import numpy as np
import open3d as o3d


class Taylor:
    def __init__(self, tape, pin, poses=None):
        """
        :param tape: It's interaction list from convention.py. call get_interactions
        :param pin: Vertices index about human parts in 3d mesh model load sitting/standing.json
        """
        self.tape = tape
        self.pin = self._convert_tag(pin)
        self.table = np.zeros(len(self.tape))
        self.poses = poses

    def update(self, poses):
        """
        :param poses: vertices ("standing", "sitting", "t", "hands-on", "curve")
        :return:
        """
        self.poses = poses

    def order(self, fast=True):
        for i, paper in enumerate(self.tape):
            _, _, tags, func, pose = paper
            # points name to index
            args = []
            for tag in tags:
                index = self.pin[tag]
                point = self.poses[pose][index]
                args.append(point)

            # function 인식
            if fast and ("circ" in func or "length" in func):
                continue
            if "circ" in func:
                stub = func.split('-')
                args.insert(0, stub[-1])
            value = getattr(self, func)(*args)
            self.table[i] = value
        return self.table

    def _convert_tag(self, pin):
        standing, sitting = pin
        tag = dict()
        for key, value in standing:
            _, eng, direction = self._separate_key(key)
            tag[eng + direction] = value

        for key, value in sitting:
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


