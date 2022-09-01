"""Data parser for knapsack problem.

References:
    - https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html

Author:
    - Name: Wonjun Yoo
    - Email: ehdrhks0000@naver.com
"""
from dataclasses import dataclass
from typing import List
import operator

import os
import tqdm

from problems import Problem, Problems

@dataclass
class KnapsackData(Problem):
    capacity: int
    profits: List[int]
    weights: List[int]    

    def get_initial_state(self) -> List[bool]:
        """Get initial state of select none."""
        return [False for i in range(len(self.profits))]

    def evaluate(self, selection: List[bool]) -> float:
        """Do evaluate for given selection."""
        assert len(selection) == len(self.weights)

        selection: List[int] = list(map(int, selection))
        selection_profit = sum(map(operator.mul, selection, self.profits))
        selection_weight = sum(map(operator.mul, selection, self.weights))
        
        if selection_weight > self.capacity: return 0.0
        else: return float(selection_profit)

    def draw(self, selection: List[bool]) -> None:
        """Print selection."""
        assert len(selection) == len(self.weights)

        sel_index = [index+1 for index in range(len(selection)) if selection[index]]
        print(f"selections : {sel_index}")        


class Knapsack(Problems):
    """Data parser for knapsack problem.
    References:
        - https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html
    """

    def _parse_data(self) -> List[KnapsackData]:
        """Parse data."""
        problem_basenames = [
            file.name.split("_")[0]
            for file in self.data_path.iterdir()
            if file.name.endswith('_c.txt')         
        ]

        problems = [
            self._parse_knapsack_file(basename)                
            for basename in tqdm.tqdm(sorted(problem_basenames), desc="Parsing Data:")
        ]
        return problems

    def _parse_knapsack_file(self, basename: str):
        """Parse one knapsack data."""
        capacity_file = self.data_path.joinpath(f"{basename}_c.txt")
        weights_file = self.data_path.joinpath(f"{basename}_w.txt")
        profits_file = self.data_path.joinpath(f"{basename}_p.txt")

        capacity_read = self._read_integers(capacity_file)
        weights_read = self._read_integers(weights_file)
        profits_read = self._read_integers(profits_file)

        assert len(capacity_read) == 1
        assert len(weights_read) == len(profits_read)       

        return KnapsackData(capacity = capacity_read[0],
                            profits = profits_read,
                            weights = weights_read)

    def _read_integers(self, file_path) -> List[int]:
        """Read interger list from file."""
        assert os.path.exists(file_path)

        res = []

        with open(file_path) as file:
            for line in file:                
                line = line.strip()
                if not line: continue
                res.append(int(line))

        return res
