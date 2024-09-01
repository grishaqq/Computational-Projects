from pysat.formula import *
from pysat.solvers import Solver
from statistics import mean
from bisect import bisect_left
from scipy.optimize import curve_fit
import numpy as np
from cnf_generator import generate_cnf
from utils import *


def is_cnf_satisfiable(cnf):
    """returns 1 if formula is satisfiable, 0 otherwise"""
    s = Solver()
    s.append_formula(cnf.clauses)
    s.solve()
    if s.get_model() != None:
        return 1
    return 0


def sample_cnf_satisfiability(k, n, m, evaluate_cnf=is_cnf_satisfiable, attempts=10):
    """returns average result of evaluate_cnf of generated cnfs of given k, n, m"""
    return mean(evaluate_cnf(generate_cnf(k, n, m)) for _ in range(attempts))


def plot_certainty_line(perc, p, proj, do_plot=True):
    """plots certainty line/ to the left of certainty line CNFs are satisfible with chance of perc
    and returns its coefficients
    """
    # for each m find N such that for all n < N p(m, n) < min%
    # for each m find N such that for all n > N p(m, n) > max%
    certain_ns = []
    for m in proj.mrange:
        ind = bisect_left(p[proj.encode_m(m)], perc)
        certain_ns.append(proj.decode_n(ind))
    params, cov = curve_fit(linear_approximation, list(proj.mrange), certain_ns)
    certain_a = params[0]
    certain_b = params[1]

    if do_plot:
        # Define the range of m for plotting the line
        m_values = np.linspace(min(proj.mrange), max(proj.mrange), 10)

        # Calculate corresponding m values using the fitted parameters
        n_values = linear_approximation(m_values, certain_a, certain_b)

        ax3d.plot(
            n_values,
            m_values,
            np.full(n_values.size, perc),
            label="Line",
            color="b",
            linewidth=3,
        )
    return certain_a, certain_b


def plot_experiment_points(ns, ms, ps, color="r"):
    """plots points in n/m/p on ax3d axes"""
    # Plot the points
    ax3d.scatter(ns, ms, ps, c=color, marker="o")

    # Set labels
    ax3d.set_xlabel("n Label")
    ax3d.set_ylabel("m Label")
    ax3d.set_zlabel("p Label")


def set_experiments(proj, evaluate_cnf=is_cnf_satisfiable):
    """returns three lists, such that i_th element in each forms a point on n/m/p axes,
    (+ returns 2d list of values of p's instead of 1d list) where p is average result of evaluate_cnf
    """
    ns = []
    ms = []
    ps = []
    p = [[0 for _ in proj.nrange] for _ in proj.mrange]
    print("Setting experiments ... ")
    for n in proj.nrange:
        print(f"n: {n}")
        for m in proj.mrange:
            print(f"  m: {m}")
            ns.append(n)
            ms.append(m)
            r = sample_cnf_satisfiability(proj.k, n, m, evaluate_cnf=evaluate_cnf)
            ps.append(r)
            p[proj.encode_m(m)][proj.encode_n(n)] = r
    return ns, ms, ps, p


def plot_certainty_lines_for_ks():
    """plots 'pairs of certainty lines' for different k's / to the left of certainty
    lines most CNFs are unsatisfible (<5%), to the right most are satisfiable (>95%)"""

    krange = range(2, 6)
    colors = [
        "blue",
        "orange",
        "green",
        "red",
        "purple",
        "brown",
        "pink",
        "gray",
        "olive",
        "cyan",
    ]
    proj = Project(mmax=100, nmax=100)
    new_mmax = proj.mmax
    new_nmax = proj.nmax

    for k_temp in krange:
        new_mmax = k_temp * 100 - 100
        temp_proj = Project(mmax=new_mmax, nmax=new_nmax, mstep=k_temp, k=k_temp)
        ns, ms, ps, p = set_experiments(temp_proj)
        a_min, b_min = plot_certainty_line(0.03, p, temp_proj, do_plot=False)
        a_max, b_max = plot_certainty_line(0.97, p, temp_proj, do_plot=False)
        # plot two lines with ax+b = y

        n_values = np.linspace(0, 100, 5)

        # Calculate corresponding y values for the lines y = ax + b
        m_values_min = a_min * n_values + b_min
        m_values_max = a_max * n_values + b_max

        # Plot the lines in the 2D subplot
        ax2d.plot(
            n_values,
            m_values_min,
            label=f"m = {a_min}n + {b_min}",
            color=colors[k_temp - 2],
        )
        ax2d.plot(
            n_values,
            m_values_max,
            label=f"m = {a_max}n + {b_max}",
            color=colors[k_temp - 2],
        )

        new_nmax = round(0.75 * new_nmax)

    ax2d.set_xlabel("n")
    ax2d.set_ylabel("m")
    ax2d.legend()
