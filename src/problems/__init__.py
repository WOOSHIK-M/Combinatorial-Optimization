"""Call problem.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""

from problems.problem import Problem, Problems
from problems.tsp import TSP

__all__ = [
    "Problems",
    "Problem",
    "TSP",
]


def call_problem(problem: str) -> Problems:
    """Call problem."""
    if problem == "tsp":
        return TSP()

    raise KeyError(f"Please import {problem.upper()} class ...")
