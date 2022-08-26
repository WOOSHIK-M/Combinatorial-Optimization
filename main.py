"""
The main script to run our solvers.

Our github: https://github.com/WOOSHIK-M/Combinatorial-Optimization

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""
import argparse

from problems import call_problem
from solvers import call_solver

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", type=str, default="tsp", help="problem name")
    parser.add_argument("--solver", type=str, default="sa", help="solver name")
    args = parser.parse_args()

    # get problem & solver
    problems = call_problem(args.problem)
    solver = call_solver(args.solver)

    # do optimization
    problem = problems.get_evaluation_data()
    optimal_solution = solver.get_optimal_solution(problem)
    problem.draw(optimal_solution)
