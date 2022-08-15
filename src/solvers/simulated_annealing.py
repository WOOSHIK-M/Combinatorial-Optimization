"""Simulated annealing optimization.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""

from typing import Any

from solvers.solver import Solver
from structure import TSPData


class SimulatedAnnealing(Solver):
    """Simulated annealing."""

    def __init__(
        self,
        init_temp: float = 1e-3,
        thres_temp: float = 1e-1,
        n_iter: int = 150,
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

    def optimize(self, problem: TSPData) -> Any:
        """Do optimization."""
        cur_temp = self.init_temp
