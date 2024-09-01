import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
from utils import cube_volume, inside_sphere, generate_point, calc_err


def iterations_to_reach_error(err_to_reach, d, inside_shape=inside_sphere):
    """returns number of generated points(regular mc) it took to reach given error(for a sphere in d dimensions)"""
    in_point_cnt = 0
    total_point_cnt = 1
    cube_vol = cube_volume(d)
    if inside_shape(generate_point(d)):
        in_point_cnt += 1
    while calc_err(in_point_cnt / total_point_cnt * cube_vol, d) > err_to_reach:
        total_point_cnt += 1
        if inside_shape(generate_point(d)):
            in_point_cnt += 1

    return total_point_cnt


def sample_iterations_to_reach_error(err_to_reach, d, n=100):
    """returns mean number of generated points(regular mc) it took to reach given error(for a sphere in d dimensions)"""
    return mean(iterations_to_reach_error(err_to_reach, d) for i in range(n))


def plot_iters_vs_d(err_to_reach, min_dim=2, max_dim=15, n=100):
    """plots mean number of generated points(regular mc) it took to reach given error(for a sphere in d dimensions) against d"""
    dims = np.arange(min_dim, max_dim + 1)
    iters_num = np.fromiter(
        (
            sample_iterations_to_reach_error(err_to_reach=err_to_reach, d=d, n=n)
            for d in dims
        ),
        dtype=float,
    )
    plt.plot(dims, iters_num)
    plt.title(f"number of iterations for each d to reach error {err_to_reach}")
    plt.xlabel("d")
    plt.ylabel("#iteration")
    plt.show()
