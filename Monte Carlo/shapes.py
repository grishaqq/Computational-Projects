import numpy as np
import random


# to implement: Point class/ used numpy array of length d to represent a point of d dimensions


class Shape:
    pass


class Plane:
    """random plane class"""

    # Sum(a_i*p_i) + b = 0
    def __init__(self, dim):
        self.dim = dim
        # self.a = a
        # if (a == np.zeros(dim)).all() : self.a = np.random.uniform(-1, 1, dim)
        # self.b = b
        # if b == -1 : self.b = random.uniform(-1, 1)

        # self.a = a
        # self.b = b
        self.a = np.random.uniform(-1, 1, dim)
        self.b = random.uniform(-1, 1)

    def point_above_plane(self, pt):
        """returns true is point is above plane, false otherwise"""
        res = 0
        for i in range(self.dim):
            res += self.a[i] * pt[i]
        return res + self.b > 0


class Polytope(Shape):
    """random polytope class"""

    # assuming all hyper-planes are non-parallel means polytope has d+1 sides + bounded by ±1
    def __init__(self, dim):  # dimension, coordinate, vectors
        self.dim = dim
        # self.ps = ps
        self.ps = [Plane(dim) for _ in range(dim + 1)]

    def point_in_polytope(self, pt):
        """returns true if point is inside the polytope"""
        # assuming 0 vector is in polytope
        o = np.zeros(self.dim)
        for c in pt:
            if abs(c) > 1:
                return False
        for pln in self.ps:
            if pln.point_above_plane(o) != pln.point_above_plane(pt):
                return False
        return True

    def maximum_radius_to_fit(self):
        """returns the length of biggest possible radius such that the circle wouldn't cross out"""
        res = 1.0
        for pln in self.ps:
            wl = 0
            for w in pln.a:
                wl += w * w
            res = min(res, abs(pln.b) / np.sqrt(wl))
        return res
