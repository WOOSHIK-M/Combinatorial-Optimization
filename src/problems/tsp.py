"""Data parser for traveling salesman problem.

References:
    - http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""
import random
import re
from collections import namedtuple
from dataclasses import dataclass
from pathlib import PosixPath
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import tqdm

from problems import Problem, Problems

# named tuples
City = namedtuple("City", "index x y")


@dataclass
class TSPData(Problem):
    name: str
    cities: List[City]
    adj_mat: np.ndarray

    def get_initial_state(self, is_random: bool = True) -> List[int]:
        """."""
        tour = list(range(self.n_cities))
        if is_random:
            random.shuffle(tour)
        return tour

    def evaluate(self, tour: List[int]) -> float:
        """Do evaluate for the given tour."""
        assert len(tour) == self.adj_mat.shape[0]

        evaluate_tour = tour + [tour[0]]
        distance = 0.0
        for idx, source in enumerate(evaluate_tour[:-1]):
            destination = evaluate_tour[idx + 1]
            distance += self.adj_mat[source, destination]
        return -distance

    def draw(self, tour: List[int]) -> None:
        """Draw the tour path."""
        assert len(tour) == self.adj_mat.shape[0]

        evaluate_tour = tour + [tour[0]]
        for idx, source in enumerate(evaluate_tour[:-1]):
            destination = evaluate_tour[idx + 1]

            _, source_x, source_y = self.cities[source]
            _, destination_x, destination_y = self.cities[destination]

            plt.scatter(source_x, source_y)
            plt.arrow(
                source_x,
                source_y,
                destination_x - source_x,
                destination_y - source_y,
                width=0.008,
                length_includes_head=True,
            )
        plt.title(f"Tour Length: {self.evaluate(tour):.2f}")
        plt.savefig("TSP.png")
        plt.close()

    @property
    def n_cities(self) -> int:
        """Get the number of cities."""
        return self.adj_mat.shape[0]


class TSP(Problems):
    """Data parser for tsp problem.

    Notes:
        - ignore some files which is written with edge_weight_format
          to make parsing easier.

    References:
        - http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf
    """

    def _parse_data(self) -> List[TSPData]:
        """Parse data."""
        files = [
            file.name.split(".")[0]
            for file in self.data_path.iterdir()
            if file.suffix == ".tsp"
        ]

        problems = [
            self._parse_tsp_file(self.data_path.joinpath(f"{file}.tsp"))
            for file in tqdm.tqdm(sorted(files)[:1], desc="Parsing Data:")
        ]
        return problems

    def _parse_tsp_file(self, file_path: PosixPath) -> TSPData:
        """Parse data from .tsp file."""
        with open(file_path, "r") as file:
            contents = file.read()
            name = re.findall(r"NAME\s*:\s*(.+)\n", contents)[0]
            n_cities = int(re.findall(r"DIMENSION\s*:\s*(.+)\n", contents)[0])

            # parse cities
            if "NODE_COORD_SECTION" in contents:
                city_block = self._get_city_block("NODE_COORD_SECTION", contents)
            elif "DISPLAY_DATA_SECTION" in contents:
                city_block = self._get_city_block("DISPLAY_DATA_SECTION", contents)
            else:
                raise NotImplementedError(f"Unknown format...{file_path}")

            cities = self._parse_cities(city_block)
            assert n_cities == len(cities), "Wrong regex to parse .tsp file..."

            adj_mat = self._make_adjacency_matrix(cities)
        return TSPData(name=name, cities=cities, adj_mat=adj_mat)

    def _get_city_block(self, section_name: str, contents: str) -> str:
        """Get city informations of the given section."""
        pattern = rf"{section_name}\s*(\n.+)+(\nEOF)*"
        city_block = re.search(pattern, contents).group().split("\n")
        if "EOF" in city_block[-1]:
            city_block.pop()
        return city_block

    def _parse_cities(self, city_block: str) -> List[City]:
        """Parse cities from the given text.

        It has the below format.
            {idx} {x_coordinate} {y_coordinate}
            ...
        """
        cities = []
        for line in city_block[1:]:
            city_idx, loc_x, loc_y = line.split()
            city = City(index=int(city_idx), x=float(loc_x), y=float(loc_y))
            cities.append(city)
        return cities

    def _make_adjacency_matrix(self, cities: List[City]) -> np.ndarray:
        """."""
        n_cities = len(cities)
        adj_mat = np.zeros((n_cities, n_cities))

        # TODO(wooshik.myung): need to accelerate the below calculation
        for i, city_i in enumerate(cities[:-1]):
            for j, city_j in enumerate(cities[i + 1 :], start=i + 1):
                weight = abs(city_i.x - city_j.x) + abs(city_i.y - city_j.y)
                adj_mat[i, j] = weight
                adj_mat[j, i] = weight
        return adj_mat

    def _parse_tour(self, file_path: PosixPath) -> None:
        """Parse data from .tour file."""
        # TODO(wooshik.myung): get the optimal path if it exists
        assert False
