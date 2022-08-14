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
from typing import Any, List, Tuple

import numpy as np

from structure import TSP, City


class DataParser(metaclass=ABCMeta):

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

        for file in sorted(files):
            tsp = self._parse_tsp_file(self.data_path.joinpath(f"{file}.tsp"))

    def _parse_tsp_file(self, file_path: PosixPath) -> TSP:
        """Parse data from .tsp file."""
        print(file_path)

        with open(file_path, "r") as file:
            contents = file.read()

            # parse data
            if "NODE_COORD_SECTION" in contents:
                tsp = self._parse_node_coord_section(contents)
            elif "DISPLAY_DATA_SECTION" in contents:
                tsp = self._parse_display_data_section(contents)
            else:
                raise NotImplementedError(f"Unknown format...{file_path}")
        return tsp

    def _parse_node_coord_section(self, contents: str) -> TSP:
        """Parse cities if the file contains node coordinates."""
        name = re.findall(r"NAME\s*:\s*(.+)\n", contents)[0]
        n_cities = int(re.findall(r"DIMENSION\s*:\s*(.+)\n", contents)[0])

        cities = []
        city_block = re.search(
            r"NODE_COORD_SECTION\s*(\n.+)+(\nEOF)*", contents
        ).group()
        city_blocks = city_block.split("\n")
        if "EOF" in city_blocks[-1]:
            city_blocks.pop()

        for line in city_blocks[1:]:
            city_idx, x, y = line.split()
            city = City(index=int(city_idx), x=float(x), y=float(y))
            cities.append(city)
        assert n_cities == len(cities), "Wrong regex to parse .tsp file..."

        adj_mat = np.zeros((n_cities, n_cities))
        # for i, city_i in enumerate(cities[:-1]):
        #     for j, city_j in enumerate(cities[i + 1 :], start=i + 1):
        #         weight = abs(city_i.x - city_j.x) + abs(city_i.y - city_j.y)
        #         adj_mat[i, j] = weight
        #         adj_mat[j, i] = weight
        return TSP(name=name, adj_mat=adj_mat)

    def _parse_display_data_section(self, contents: str) -> TSP:
        """Parse cities if the file contains display data."""
        name = re.findall(r"NAME\s*:\s*(.+)\n", contents)[0]
        n_cities = int(re.findall(r"DIMENSION\s*:\s*(.+)\n", contents)[0])

        display_data_section = re.search(
            r"DISPLAY_DATA_SECTION\s*(\n.+)+(\nEOF)*", contents
        ).group()
        city_blocks = display_data_section.split("\n")
        if "EOF" in city_blocks[-1]:
            city_blocks.pop()

        cities = []
        for line in display_data_section.split("\n")[1:-1]:
            city_idx, x, y = line.split()
            city = City(index=int(city_idx), x=float(x), y=float(y))
            cities.append(city)

        adj_mat = np.zeros((n_cities, n_cities))
        # for i, city_i in enumerate(cities[:-1]):
        #     for j, city_j in enumerate(cities[i + 1 :], start=i + 1):
        #         weight = abs(city_i.x - city_j.x) + abs(city_i.y - city_j.y)
        #         adj_mat[i, j] = weight
        #         adj_mat[j, i] = weight
        assert n_cities == len(cities), "Wrong regex to parse .tsp file..."
        return TSP(name=name, adj_mat=adj_mat)

    def _parse_tour(self, file_path: PosixPath) -> TSP:
        """Parse data from .tour file."""
        print(file_path)
        assert False


TSPDataParser()
