import itertools
import random
from math import comb
from random import sample, choice
from pysat.formula import *


def generate_bool():
    """returns random Bool"""
    if choice([0, 1]) == 1:
        return True
    return False


def generate_clause(k, n):
    """returns random clause (as a list)"""
    variables = range(1, n + 1)
    random_k_variables = sample(variables, k)
    random_k_variables.sort()
    for i in range(k):
        if generate_bool():
            random_k_variables[i] *= -1
    return random_k_variables


def generate_complements(l):
    """returns list of all possible minus assignments to each element of list (2^len(l))"""
    extended_list = [(x, -x) for x in l]
    return list(itertools.product(*extended_list))


def concatenate_list(l):
    """returns concatenated list of lists"""
    return list(itertools.chain.from_iterable(l))


def generate_cnf(k, n, m):  # k - length of each clause, n - variables,  m - clauses
    """returns randomly generated CNF formula, or empty CNF if not enough variables (n) for m clauses"""
    f = CNF()
    # check that number of possible clauses > m
    possible_clauses_cnt = 2**k * comb(n, k)
    if possible_clauses_cnt < m:
        f.append([])
        return f
    if possible_clauses_cnt > 4 * m:
        # if many possible clauses, it's faster to generate them one by one
        while len(f.clauses) < m:
            new_clause = generate_clause(k, n)
            if not new_clause in f.clauses:
                f.append(new_clause)
        return f
    else:
        # generate all possible clauses and pick m
        all_clauses_no_complements = list(
            itertools.combinations(list(range(1, n + 1)), k)
        )
        all_clauses = concatenate_list(
            list(generate_complements(c) for c in all_clauses_no_complements)
        )
        random.shuffle(all_clauses)
        f.extend(all_clauses[:m])
        return f
