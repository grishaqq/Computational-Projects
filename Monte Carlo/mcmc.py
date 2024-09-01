import numpy as np
from utils import var, inside_sphere, sphere_volume, init_points, gen_start_point, TPC
from shapes import Polytope
from statistics import mean
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def mcmc_generate_point(d, x):
    """generates new point from previous one according to mcmc, using global variance"""
    y = np.zeros(d)
    for j in range(d):
        y[j] = np.random.normal(x[j], var)
    return y


def mcmc_volume_approximation(p, in_points):
    """returns approximation of volume of polytope(p) given list of points inside p"""
    # finding - this doesn't generate points uniformly, ratio of points inside circle higher than in polytope 😔
    points_in_circle = 0
    r = p.maximum_radius_to_fit()
    for point in in_points:
        if inside_sphere(point, r):
            points_in_circle += 1
    return in_points.size / points_in_circle * sphere_volume(2, r)


def test_acceptance_ratio(total_point_cnt=TPC, dim=2):
    """returns approximated acceptance ratio of generated points in mcmc"""
    p = Polytope(dim=dim)
    approxs, in_points = init_points(
        total_point_cnt=total_point_cnt,
        d=dim,
        inside_shape=p.point_in_polytope,
        next_point=mcmc_generate_point,
        skip_start=True,
    )
    return in_points.size / (total_point_cnt - gen_start_point(total_point_cnt))


def sample_acceptance_ratio(total_point_cnt=TPC, n=10, dim=2):
    """returns mean of approximated acceptance ratios of generated points in mcmc"""
    return mean(test_acceptance_ratio(total_point_cnt, dim) for _ in range(n))


def plot_acceptance_ratio_vs_variance(
    dim=2, min_var=0.0, max_var=1.0, n=10, total_point_cnt=TPC, do_plot=True
):
    """plots approximated acceptance ratio vs variance and returns estimated perfect variance"""
    global var
    vars_to_test = np.linspace(min_var, max_var, num=n)
    acc_ratios = np.zeros(n)
    for i in range(vars_to_test.size):
        var = vars_to_test[i]
        acc_ratios[i] = sample_acceptance_ratio(
            total_point_cnt=total_point_cnt, dim=dim
        )
    inv_interp = interp1d(acc_ratios, vars_to_test)
    est_perf_var = inv_interp(0.5)
    if do_plot:
        plt.xlabel("Variance")
        plt.ylabel("acceptance ratio")
        plt.title(f"acceptance ratio vs Variance at {dim} dimensions")
        plt.plot(vars_to_test, acc_ratios)
        plt.plot(np.array([est_perf_var]), np.array([0.5]), "o", color="red")
        plt.show()
    return est_perf_var


def plot_perfect_variance_vs_dimension(
    min_dim=2, max_dim=10, n=10, total_point_cnt=TPC
):
    """plots estimated perfect variance graph vs dimension"""
    # perfect variance is variance such that accepted ratio is 50%
    dims = np.arange(min_dim, max_dim + 1)
    perf_vars = np.zeros(max_dim - min_dim + 1)
    for dim in dims:
        perf_vars[dim - min_dim] = plot_acceptance_ratio_vs_variance(
            dim=dim, do_plot=False, total_point_cnt=total_point_cnt, n=n
        )
        print(f"{dim} {perf_vars[dim-min_dim]}")
    plt.xlabel("dimensions")
    plt.ylabel("perfect variance ratio")
    plt.title(f"perfect variance ratio vs dimension")
    plt.plot(dims, perf_vars)
    plt.show()
