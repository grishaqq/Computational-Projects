import math
import numpy as np

TPC = 1000000
var = 0.5


def sphere_volume(d, r=1):
    """returns sphere volume of radius r in d dimensions"""
    if d == 0:
        return 1
    if d == 1:
        return 2 * r
    return (2 * math.pi / d * r**2) * sphere_volume(d - 2, r)


def cube_volume(d):
    """returns volume of cube in d dimensions"""
    return 2**d


def calc_err(res, d=2):
    """returns relative error of calculated volume of sphere"""
    volume = sphere_volume(d)
    return abs(res - volume) / volume


def root_aprox(x, a, b):
    """returns a/sqrt(x) + b"""
    return 1 / np.sqrt(x) * a + b


def linear_aprox(x, a, b):
    """returns x*a + b"""
    return x * a + b


def horz_aprox(x, c):
    """returns c"""
    return 0 * x + c


def inside_sphere(c, r=1.0):
    """returns true if point is inside sphere of radius r"""
    d = sum(x * x for x in c)
    return d <= r * r


def generate_point(d=2, pp=object()):
    """returns random point in d dimensions, range of coordinates is (-1, 1)"""
    return np.random.uniform(-1, 1, d)


def init_points(
    total_point_cnt=1000000,
    d=2,
    inside_shape=inside_sphere,
    next_point=generate_point,
    skip_start=False,
):
    """returns numpy arrays of approximations of volume over time and points inside shape"""
    # init of generated points and errors
    approxs = np.empty(total_point_cnt)
    points = np.empty(total_point_cnt, dtype=object)
    start_point = gen_start_point(total_point_cnt)
    point_cnt = 0
    in_point_cnt = 0
    prev_point = np.zeros(d)
    cube_vol = cube_volume(d)
    for i in range(total_point_cnt):
        point = next_point(d, prev_point)
        if inside_shape(point):
            if not skip_start or i >= start_point:
                in_point_cnt += 1
            prev_point = point
        point_cnt += 1
        approxs[i] = in_point_cnt / point_cnt * cube_vol
        points[i] = point
    in_points = np.empty(in_point_cnt, dtype=object)
    j = 0
    for i in range(total_point_cnt):
        if inside_shape(points[i]) and (not skip_start or i >= start_point):
            in_points[j] = points[i]
            j += 1

    return approxs, in_points


def gen_it_errs(approxs, d):
    """(function was made for numpy array, but can be used for one approximation)
    returns numpy array of approximation errors over time (for spheres in d dimensions)
    """
    return calc_err(approxs, d)


def gen_start_point(tp_cnt):
    """returns number of points to skip (mainly for mcmc)"""
    return round(tp_cnt / 10)
