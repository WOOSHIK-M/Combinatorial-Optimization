"""Data parser.

Data format:
    - {problem}.zip is required

References:
    - TSP: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""
import re
import zipfile
from abc import ABCMeta, abstractmethod
from pathlib import Path, PosixPath
from typing import Any, List

import numpy as np

from structure import TSP, City


class DataParser(metaclass=ABCMeta):
    """Parse the given problem.

    If you want to define a new problem and the data is constructed,
    the data files need to be zipped as {problem_name}.zip.
    """

    DATA_DIR = "data"
    ZIP_EXTENSION = ".zip"

    def __init__(self, problem="tsp") -> None:
        """Initialize."""
        self.data_path = Path(self.DATA_DIR).joinpath(problem)
        if not Path.exists(self.data_path):
            self._extract_data(problem)
        self.dataset = self._parse_data()

    def _extract_data(self, problem: str) -> None:
        """Unzip the data file."""
        zip_path = self.data_path.with_suffix(self.ZIP_EXTENSION)
        assert Path.exists(zip_path), f"Unknown problem -> {problem}..."

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.DATA_DIR)

    @abstractmethod
    def _parse_data(self) -> List[Any]:
        """Parse data."""
        pass


class TSPDataParser(DataParser):
    """Data parser for tsp problem.

    References:
        - http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf
    """

    def _parse_data(self) -> List[TSP]:
        """Parse data."""
        files = [
            file.name.split(".")[0]
            for file in self.data_path.iterdir()
            if file.suffix == ".tsp"
        ]

        problems = []
        for file in sorted(files):
            tsp = self._parse_tsp_file(self.data_path.joinpath(f"{file}.tsp"))
            problems.append(tsp)
        return problems

    def _parse_tsp_file(self, file_path: PosixPath) -> TSP:
        """Parse data from .tsp file."""
        print(file_path)

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
        return TSP(name=name, adj_mat=adj_mat)

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
        # for i, city_i in enumerate(cities[:-1]):
        #     for j, city_j in enumerate(cities[i + 1 :], start=i + 1):
        #         weight = abs(city_i.x - city_j.x) + abs(city_i.y - city_j.y)
        #         adj_mat[i, j] = weight
        #         adj_mat[j, i] = weight
        return adj_mat

    def _parse_tour(self, file_path: PosixPath) -> TSP:
        """Parse data from .tour file."""
        print(file_path)
        assert False


TSPDataParser()
