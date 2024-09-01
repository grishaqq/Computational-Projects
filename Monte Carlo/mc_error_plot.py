import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from utils import (
    linear_aprox,
    init_points,
    TPC,
    inside_sphere,
    generate_point,
    gen_it_errs,
)


def plot_power_linearly(it_errs, do_plot=False):
    """plots log(err) against log(#iters) and returns linear approximation coefficients"""

    total_point_cnt = it_errs.size
    start_point = 1
    log_it_errs = np.log(it_errs)
    x_fit = np.log(
        np.linspace(start_point, total_point_cnt, (total_point_cnt - start_point))
    )
    pwr_scale_it = log_it_errs[start_point:]
    params, cov = curve_fit(linear_aprox, x_fit, pwr_scale_it)
    a, b = params
    if do_plot:
        plt.plot(x_fit, linear_aprox(x_fit, a, b))
        plt.plot(x_fit, pwr_scale_it)
        plt.xlabel("log(N)")
        plt.ylabel("log(error)")
        plt.title(f"MC scales with power approx. {a}")
        plt.show()
    return a, b


def plot_avg_power_linearly(n=30):
    """plots mean linear approximation of log(err) against log(#iters)"""
    # MC error is O(n^slope), where n is #iterations
    sum_a = 0
    sum_b = 0
    for _ in range(n):
        approxs, in_points = init_points(
            total_point_cnt=TPC,
            d=2,
            inside_shape=inside_sphere,
            next_point=generate_point,
            skip_start=False,
        )
        it_errs = gen_it_errs(approxs, d=2)
        a, b = plot_power_linearly(it_errs, do_plot=False)
        sum_a += a
        sum_b += b
        print(f"{a} {b}")
    avg_a = sum_a / n
    avg_b = sum_b / n
    x_fit = np.linspace(0, 15, 15)
    plt.plot(x_fit, linear_aprox(x_fit, avg_a, avg_b))
    plt.xlabel("log(N) - ish")
    plt.ylabel("log(error) - ish")
    plt.title(f"MC scales with power approx. {avg_a}")
    plt.show()
