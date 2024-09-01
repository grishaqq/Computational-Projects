from iters_needed_plot import *
from mc_error_plot import *
from error_vs_iters_plot import *
from utils import *
from shapes import *
from points_plot_2d import *
from mcmc import *

p = Polytope(dim=2)
"""
Project goal:
Look into how Monte Carlo works when approximating volumes


"""
# p = Polytope(dim = 2, ps = np.array([Plane(dim = 2, a = np.array([1, -1]), b = -1)]))
# p = Polytope(dim = 2, ps = np.array([Plane(dim = 2, a = np.array([0, 1]), b = 100)]))


if False:
    # estimates number of iterations to reach relative error of 0.1 in circles of different dimensions
    plot_iters_vs_d(0.1, min_dim=2, max_dim=10)

if False:
    # estimates volume using MCMC / PS. approxs are invalid for MCMC
    approxs, in_points = init_points(
        total_point_cnt=TPC,
        d=2,
        inside_shape=p.point_in_polytope,
        next_point=mcmc_generate_point,
        skip_start=True,
    )
    print(mcmc_volume_approximation(p, in_points=in_points))
    plot_points_2d(p, in_points)  # for 2d only


if False:
    # estimates volume using regular MC
    approxs, in_points = init_points(
        total_point_cnt=TPC,
        d=2,
        inside_shape=p.point_in_polytope,
        next_point=generate_point,
        skip_start=False,
    )
    print(approxs[-1])
    plot_points_2d(p, in_points)  # for 2d only

if False:
    # MC scale for 2d circle and relative error graph
    approxs, in_points = init_points(
        total_point_cnt=TPC,
        d=2,
        inside_shape=inside_sphere,
        next_point=generate_point,
        skip_start=False,
    )
    it_errs = gen_it_errs(approxs, d=2)
    plot_avg_power_linearly(n=50)
    # plot_power_linearly(it_errs, do_plot=True) #this line is mostly irrelevant
    plot_errors_vs_iterations(it_errs)

if False:
    # acceptance ration vs var
    plot_acceptance_ratio_vs_variance(dim=2, max_var=5, total_point_cnt=TPC)

if False:
    # Perfect variance vs d graph
    plot_perfect_variance_vs_dimension(max_dim=20, total_point_cnt=TPC)
