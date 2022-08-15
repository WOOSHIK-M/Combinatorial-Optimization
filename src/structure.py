"""Data structure.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""
from collections import namedtuple
from dataclasses import dataclass
from typing import List

import numpy as np

# named tuples
City = namedtuple("City", "index x y")


@dataclass
class TSPData:
    name: str
    cities: List[City]
    adj_mat: np.ndarray

    @property
    def n_cities(self) -> int:
        """Get the number of cities."""
        return self.adj_mat.shape[0]

    @property
    def evaluate(self, tour: List[int]) -> float:
        """Do evaluate for the given tour."""
        assert len(tour) == self.adj_mat.shape[0]

        distance = 0.0
        tour += tour[0]
        for idx, source in enumerate(tour[:-1]):
            destination = tour[idx + 1]
            distance += self.adj_mat[source, destination]
        return distance
