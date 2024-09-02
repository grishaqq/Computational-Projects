import matplotlib.pyplot as plt
from pysat.formula import *
import random
import numpy as np

temp = 0.015
TEMP_M = 0.999
r = 0.3  # energy constant / if clause is satisfied multiple times, its energy is 1 + r + r^2 + ...
# bc = 1.5 # bernouli constant for switching up multiple variables in modify_guess
no_sat_energy = -2
EPS = 4 * np.finfo(float).eps
fig3d = plt.figure()
fig2d = plt.figure()
ax3d = fig3d.add_subplot(111, projection="3d")
ax2d = fig2d.add_subplot(111)


class Project:
    """project class defining its n/m/k values"""

    def __init__(self, mmin=1, nmin=1, mmax=100, nmax=100, mstep=2, nstep=2, k=2):
        self.mmin = mmin
        self.nmin = nmin
        self.mmax = mmax
        self.nmax = nmax
        self.mstep = mstep
        self.nstep = nstep
        self.mrange = range(self.mmin, self.mmax + 1, self.mstep)
        self.nrange = range(self.nmin, self.nmax + 1, self.nstep)
        self.k = k

    def update_m(self, mmin=None, mmax=None, mstep=None):
        if mmin is not None:
            self.mmin = mmin
        if mmax is not None:
            self.mmax = mmax
        if mstep is not None:
            self.mstep = mstep
        self.mrange = range(self.mmin, self.mmax + 1, self.mstep)

    def update_n(self, nmin=None, nmax=None, nstep=None):
        if nmin is not None:
            self.nmin = nmin
        if nmax is not None:
            self.nmax = nmax
        if nstep is not None:
            self.nstep = nstep
        self.nrange = range(self.nmin, self.nmax + 1, self.nstep)

    def encode_m(self, m):
        """returns encoded value of m (to save space in lists/arrays)"""
        return int((m - self.mmin) / self.mstep)

    def encode_n(self, n):
        """returns encoded value of n (to save space in lists/arrays)"""
        return int((n - self.nmin) / self.nstep)

    def decode_m(self, encoded_m):
        """returns decoded value of m (to save space in lists/arrays)"""
        return encoded_m * self.mstep + self.mmin

    def decode_n(self, encoded_n):
        """returns decoded value of n (to save space in lists/arrays)"""
        return encoded_n * self.nstep + self.nmin


def linear_approximation(x, a, b):
    """returns x * a + b"""
    return x * a + b


def cnf_to_wcnf(cnf):
    """returns WCNF formula equivalent to CNF"""
    wcnf = WCNF()
    for c in cnf.clauses:
        wcnf.append(c, weight=1)
    return wcnf


def decision(probability):
    """returns True with probability 'probability', False otherwise"""
    return random.random() < probability


def sign(x):
    """returns sign of x (0 if x = 0)"""
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
