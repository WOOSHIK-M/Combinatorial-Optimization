"""Call solver.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""
from problems import problem
from solvers.simulated_annealing import SimulatedAnnealing
from solvers.solver import Solver

__all__ = [
    "Solver",
    "SimulatedAnnealing",
]


def call_solver(solver: str) -> Solver:
    """Call solver."""
    if solver == "sa":
        return SimulatedAnnealing()

    raise KeyError(f"Please import {solver.capitalize()} class ...")
