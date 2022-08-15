"""Simulated annealing optimization.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""

import random
from typing import Any

import numpy as np

from problems import Problem
from solvers.solver import Solver


class SimulatedAnnealing(Solver):
    """Simulated annealing."""

    def __init__(
        self,
        init_temp: float = 1e-3,
        thres_temp: float = 1e-5,
        n_iter: int = 1000,
        cooling_factor: float = 0.95,
    ) -> None:
        """Initialize.

        Args:
            - init_temp: initial temperature
            - thres_temp: threshold temperature
            - n_iter: the number of iterations for each temperature
            - cooling_factor: temperature reduction ratio
        """
        self.init_temp = init_temp
        self.thres_temp = thres_temp
        self.n_iter = n_iter
        self.cooling_factor = cooling_factor

    def get_optimal_solution(self, problem: Problem) -> Any:
        """Do optimization."""
        cur_state = problem.get_initial_state()
        cur_temp = self.init_temp
        cur_reward = problem.evaluate(cur_state)

        best_state, best_reward = cur_state.copy(), cur_reward

        indices = list(range(len(cur_state)))
        while cur_temp >= self.thres_temp:
            print(
                f"cur_temp: {cur_temp:.4f}, "
                f"cur_reward: {cur_reward:.4f}, "
                f"best_reward: {best_reward:.4f}"
            )

            for _ in range(self.n_iter):
                idx_0, idx_1 = np.random.choice(indices, 2)

                tmp_state = cur_state.copy()
                tmp_state[idx_0], tmp_state[idx_1] = tmp_state[idx_1], tmp_state[idx_0]
                tmp_reward = problem.evaluate(tmp_state)

                if self._accept_or_not(cur_temp, cur_reward, tmp_reward):
                    cur_state, cur_reward = tmp_state.copy(), tmp_reward

                    if tmp_reward > best_reward:
                        best_state, best_reward = cur_state.copy(), cur_reward

            cur_temp *= self.cooling_factor
        return best_state

    def _accept_or_not(
        self,
        cur_temp: float,
        cur_reward: float,
        tmp_reward: float,
    ) -> bool:
        """."""
        return tmp_reward > cur_reward
