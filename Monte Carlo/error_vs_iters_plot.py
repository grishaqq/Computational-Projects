from utils import gen_start_point, root_aprox, inside_sphere
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np


def plot_errors_vs_iterations(it_errs):
    """plots error vs iteration graph + fits [1/sqrt(#iters) + c] curve"""
    total_point_cnt = it_errs.size
    start_point = gen_start_point(total_point_cnt)
    x_fit = np.linspace(start_point, total_point_cnt, total_point_cnt - start_point)
    params, cov = curve_fit(root_aprox, x_fit, it_errs[start_point:])
    a = params[0]
    b = params[1]
    y_fit = root_aprox(x_fit, a, b)
    plt.plot(x_fit, y_fit)
    plt.plot(x_fit, it_errs[start_point:])
    plt.xlabel("N")
    plt.ylabel("relative error")
    plt.show()
