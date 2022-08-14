"""
The main script to run our solvers.

Our github: https://github.com/WOOSHIK-M/Combinatorial-Optimization

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""
import argparse

from problems import call_problem

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", type=str, default="tsp", help="problem name")
    args = parser.parse_args()

    # get dataset of the given problem
    problem = call_problem(args.problem)
