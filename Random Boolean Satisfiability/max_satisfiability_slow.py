from pysat.formula import *
from utils import *
from pysat.examples.rc2 import RC2


def max_satisfiability(cnf):
    """returns biggest possible ratio of satisfied clauses in given cnf"""
    if cnf.clauses == [[]]:
        return 0
    wcnf = cnf_to_wcnf(cnf)
    rc2 = RC2(wcnf)
    rc2.compute()
    t = len(cnf.clauses)
    return (t - rc2.cost) / t
