from pysat.formula import *
import matplotlib.pyplot as plt
from cnf_generator import *
from utils import *
from max_satisfiability_experiments import *
from max_satisfiability_slow import *
from satisfiability_experiments import *

# k - length of each clause, n - variables,  m - clauses
# more clauses(m) - less likely to be satisfiable
# more variables(n) - more likely to be satisfiable

# proj = Project()


if False:
    # plots n/m/p graph, where is p is the probability of random cnf being satisfiable
    # + certainty lines
    # value of k is set in proj (it's k = 2)
    proj = Project(mmax=100, nmax=100)
    ns, ms, ps, p = set_experiments(proj, is_cnf_satisfiable)
    plot_experiment_points(ns, ms, ps)
    plot_certainty_line(0.03, p, proj, True)
    plot_certainty_line(0.97, p, proj, True)
    plt.show()

if False:
    # plots certainty lines for k's in range [2..5]
    plot_certainty_lines_for_ks()
    plt.show()

if False:
    # plots n/m/p graph, where is p is the average ratio of clauses in cnf being satisfiable
    proj = Project(mmax=100, nmax=100)
    ns, ms, ps, p = set_experiments(proj, max_satisfiability)
    plot_experiment_points(ns, ms, ps, color="b")
    plt.show()

if False:
    # plots n/m/p graph, where is p is the average ratio of clauses in cnf being satisfiable
    # + can change attempts in sample_cnf_satisfiability for faster, but less consistent results
    # + can change max_tries in estimate_max_satisfiability for faster, but less consistent results
    proj = Project(mmin=1, mmax=2001, nmin=1, nmax=2001, nstep=50, mstep=50)
    ns, ms, ps, p = set_experiments(proj, estimate_max_satisfiability)
    plot_experiment_points(ns, ms, ps, color="g")
    plt.show()

if False:
    # plots n/m/p graph, where is p is the number of iterations needed of estimate_max_satisfiability to reach answer
    proj = Project(mmax=100, nmax=100)
    plot_iterations_to_reach_ans(proj, 0, False)
    plt.show()

if False:
    # plots n/m/p graph, where is p is log10 of number of iterations needed of estimate_max_satisfiability to reach answer
    proj = Project(mmax=100, nmax=100)
    plot_log_iterations_to_reach_ans(proj, 0, False)
    plt.show()

if False:
    # plots n/m/p graph, where is p is number of iterations needed of estimate_max_satisfiability to reach answer
    # yellow dots are dots that didn't damp temperature, purple dots did damp temperature
    # prints sum of p's for yellow dots followed by sum of p's for purple dots
    proj = Project(nmax=100, mmax=100, mstep=5, nstep=5)
    plot_iterations_to_reach_ans(proj, missed_clauses=0)
    plot_iterations_to_reach_ans(proj, missed_clauses=0, damp_temp=True, color="purple")
    print(
        f"number of iterations without damping temperature: {iterations_history[0]} \nnumber of iterations with damping temperature: {iterations_history[1]}"
    )
    plt.show()
    """
    number of iterations without damping temperature: 176,748,202 
    number of iterations with damping temperature: 43,668,696
    for TEMP = 0.02 / TEMP_M = 0.999 / nmax = 100 = mmax / mstep = 5 = nstep
    gives some evidence that damping temperature helps us find optimal solution faster

    number of iterations without damping temperature: 20,743,203 
    number of iterations with damping temperature: 16,296,582
    for TEMP = 0.016 / TEMP_M = 0.999

    number of iterations without damping temperature: 7,075,610 
    number of iterations with damping temperature: 4,552,950
    for TEMP = 0.013 / TEMP_M = 0.999

    number of iterations without damping temperature: 2,861,034 
    number of iterations with damping temperature: 5,083,254
    for TEMP = 0.01 / TEMP_M = 0.999

    number of iterations without damping temperature: 11,206,138 
    number of iterations with damping temperature: 6,570,280
    for TEMP = 0.0115 / TEMP_M = 0.999
    """


if True:
    # plots temperature/#iterations graph where #iterations is sum over all iterations needed in project to get perfect results
    plot_temperature_vs_iterations()
    plt.show()
