from pysat.formula import *
import numpy as np
from utils import *
import math
import random
from max_satisfiability_slow import max_satisfiability
from satisfiability_experiments import set_experiments


def generate_probability(energy_change, m, t=temp):
    """returns probability of changing energy at given temperature"""
    return min(1, math.exp((energy_change / m) / t))


def modify_guess(g):  # changes one variable to opposite value in guess and returns it
    """changes one variable's value to opposite value and returns the variable (in a list)"""
    n = g.size
    f = random.randint(0, n - 1)
    g[f] = not g[f]
    change_inds = [f]
    """for i in range(n):
        if i != f and decision(bc/n):
            change_inds.append(i)
    """
    return change_inds


def calc_satisfiability_energy_change(
    map_clause_to_satcnt, map_var_to_clause, changed_variables, guess
):
    """returns satisfied clauses number change and energy change (caused by changed variables)"""
    sat_change = 0
    energy_change = 0
    for changed_variable in changed_variables:
        for l_sign, c_i in map_var_to_clause[changed_variable]:
            # c is the clause in which changed_variable is in
            if (l_sign == 1 and guess[changed_variable]) or (
                l_sign == -1 and not guess[changed_variable]
            ):
                map_clause_to_satcnt[c_i] += 1
                if map_clause_to_satcnt[c_i] == 1:
                    sat_change += 1
                    energy_change += -no_sat_energy + 1
                else:
                    energy_change += pow(r, map_clause_to_satcnt[c_i] - 1)
            else:
                map_clause_to_satcnt[c_i] -= 1
                if map_clause_to_satcnt[c_i] == 0:
                    sat_change -= 1
                    energy_change += -1 + no_sat_energy
                else:
                    energy_change -= pow(r, map_clause_to_satcnt[c_i])
    return sat_change, energy_change


def generate_clause_energy(sat_cnt):
    """returns clause's energy (geometric series)"""
    if sat_cnt == 0:
        return no_sat_energy
    return (1 - pow(r, sat_cnt)) / (1 - r)


def estimate_max_satisfiability(cnf, until_value=-1, damp_temp=False, max_tries=10000):
    """returns maximum achieved ratio of satisfied clauses after max_tries tries if until_value is -1
    / returns number of iterations needed to reach until_value if until_value is not -1
    """
    n = cnf.nv
    m = len(cnf.clauses)
    if n == 0:
        return 0

    sat = 0
    map_var_to_clause = [set() for _ in range(n)]  # this list in unchanged
    map_clause_to_satcnt = [0] * m  # this list is modified

    # set up map_var_to_clause
    for c_i in range(m):
        for l in cnf.clauses[c_i]:
            map_var_to_clause[abs(l) - 1].add((sign(l), c_i))

    guess = np.zeros(dtype=bool, shape=n)
    # set guess[i] to be 1 if more +'s otherwise 0
    for v in range(n):
        positive_cnt = 0
        negative_cnt = 0
        for sl, _ in map_var_to_clause[v]:
            if sl == -1:
                negative_cnt += 1
            else:
                positive_cnt += 1
        if positive_cnt > negative_cnt:
            guess[v] = 1

    energy = 0  # variable irrelevant because only energy change matters
    # set up map_clause_to_satcnt
    for c_i in range(m):
        c_sat = 0
        for l in cnf.clauses[c_i]:
            if (l < 0 and not guess[-l - 1]) or (l > 0 and guess[l - 1]):
                c_sat += 1
        if c_sat > 0:
            sat += 1
        energy += generate_clause_energy(c_sat)
        map_clause_to_satcnt[c_i] = c_sat

    max_sat = sat

    i = 0
    # max_tries = max(max_tries_coeff*(n+m), 500)
    # if until_value == -1 then i < max_tries
    # if until_value != -1 then sat < until_value
    t = temp
    while (until_value == -1 and i < max_tries) or (
        until_value != -1 and (max_sat / m) + EPS < until_value
    ):
        if max_sat == m:  # when result can't be improved further
            break

        # print(f'{i} {guess} {sat}')
        changed_variables = modify_guess(guess)

        sat_change, energy_change = calc_satisfiability_energy_change(
            map_clause_to_satcnt, map_var_to_clause, changed_variables, guess
        )
        new_sat = sat + sat_change
        max_sat = max(max_sat, new_sat)
        if damp_temp and i % 10000 == 0:
            t *= TEMP_M
            if t < 0.01:
                # algorithm is likely stuck, so we restart the temperature
                t = temp
        if decision(generate_probability(energy_change, m, t)):
            # print(f'{sat} {new_sat} {energy} {new_energy} {generate_probability(energy_change, m)}w')
            sat = new_sat

        else:
            # print(f'{sat} {new_sat} {energy} {new_energy} {generate_probability(energy_change, m)}q')
            for changed_variable in changed_variables:
                guess[changed_variable] = not guess[changed_variable]
            calc_satisfiability_energy_change(
                map_clause_to_satcnt, map_var_to_clause, changed_variables, guess
            )
        i += 1
    if until_value == -1:
        return max_sat / m
    else:
        return i


def iterations_to_reach_ans(cnf, missed_clauses=0, damp_temp=False):
    """returns number of iterations to reach true answer minus #missed_clauses for given cnf using our energy solver (max-sat)"""
    ans = max_satisfiability(cnf)
    # print(ans)
    m = len(cnf.clauses)
    return estimate_max_satisfiability(
        cnf, until_value=ans * (1 - missed_clauses / m), damp_temp=damp_temp
    )


iterations_cnt = 0
iterations_history = []


def plot_iterations_to_reach_ans(
    proj, missed_clauses=0, damp_temp=False, color="y", do_plot=True
):
    """plots #iterations to reach true answer with #missed_clauses + creates iterations_history"""
    global iterations_cnt
    iterations_cnt = 0

    def iterations_to_reach_ans_with_error(cnf):
        global iterations_cnt
        iterations = iterations_to_reach_ans(cnf, missed_clauses, damp_temp=damp_temp)
        iterations_cnt += iterations
        return iterations

    ns, ms, its, _ = set_experiments(proj, iterations_to_reach_ans_with_error)
    iterations_history.append(iterations_cnt)
    if do_plot:
        ax3d.set_xlabel("n Label")
        ax3d.set_ylabel("m Label")
        ax3d.set_zlabel("#iterations to reach answer with #missed_clauses")
        ax3d.plot(ns, ms, its, color=color, marker="o", linestyle="None")


def plot_log_iterations_to_reach_ans(
    proj, missed_clauses=0, damp_temp=False, color="y"
):
    """plots log10 of #iterations to reach true answer with #missed_clauses"""

    def log_iterations_to_reach_ans_with_error(cnf):
        return math.log10(
            1 + iterations_to_reach_ans(cnf, missed_clauses, damp_temp=damp_temp)
        )

    ns, ms, its, _ = set_experiments(proj, log_iterations_to_reach_ans_with_error)
    ax3d.set_xlabel("n Label")
    ax3d.set_ylabel("m Label")
    ax3d.set_zlabel("log10 of #iterations to reach answer with #missed_clauses")
    ax3d.plot(ns, ms, its, color=color, marker="o", linestyle="None")


def plot_temperature_vs_iterations(proj=Project(nmax=100, mmax=100, mstep=7, nstep=7)):
    """plots temperature (with and without damping) against #iterations needed to get perfect results in given project"""
    global temp
    temperatures = np.linspace(0.015, 0.025, 10)
    regular_iterations = np.empty_like(temperatures)
    damped_iterations = np.empty_like(temperatures)
    print("Setting experiments ... ")
    for i in range(len(temperatures)):
        temp = temperatures[i]
        print(f"temperature: {temp}")
        plot_iterations_to_reach_ans(proj, do_plot=False)
        plot_iterations_to_reach_ans(proj, damp_temp=True, do_plot=False)
        regular_iterations[i] = iterations_history[-2]
        damped_iterations[i] = iterations_history[-1]

    ax2d.plot(
        temperatures,
        regular_iterations,
        label="iterations without temperature damping",
        color="yellow",
    )
    ax2d.plot(
        temperatures,
        damped_iterations,
        label="iterations with temperature damping",
        color="purple",
    )
    ax2d.set_xlabel("temperature")
    ax2d.set_ylabel("iterations")
    ax2d.legend()
