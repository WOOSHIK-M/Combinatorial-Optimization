"""Data parser.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""

from problems.problem import Problem
from problems.tsp import TSP


def call_problem(problem: str) -> Problem:
    """Call problem."""
    if problem == "tsp":
        return TSP()

    raise KeyError(f"Please import {problem.upper()} class ...")
