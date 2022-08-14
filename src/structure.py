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
    adj_mat: np.ndarray

    @property
    def n_cities(self) -> int:
        """Get the number of cities."""
        return self.adj_mat.shape[0]
