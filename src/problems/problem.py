"""Data parser.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""

import random
import zipfile
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, List

import numpy as np


class Problem(metaclass=ABCMeta):
    """."""

    @abstractmethod
    def get_initial_state(self) -> List[int]:
        """."""
        pass

    @abstractmethod
    def evaluate(self, **_: Any) -> float:
        """."""
        pass

    @abstractmethod
    def draw(self, **_: Any) -> None:
        """."""
        pass


class Problems(metaclass=ABCMeta):
    """Abstract class of the problem.

    The format of inherited problem class.
        - the class name must be the upper case of the problem name.
        - the dataset name must be zipped as {problem_name}.zip file
          and the file name is lower case of the problem name.
    """

    DATA_DIR = "data"
    ZIP_EXTENSION = ".zip"

    def __init__(self) -> None:
        """Initialize."""
        problem_name = self.__class__.__name__

        self.data_path = Path(self.DATA_DIR).joinpath(problem_name)
        if not Path.exists(self.data_path):
            self._extract_data(problem_name)
        self.dataset: List[Problem] = self._parse_data()

    def get_training_data(
        self, n_data: int = 1, random_select: bool = True
    ) -> List[Problem]:
        """."""
        if random_select:
            return np.random.choice(self.dataset, n_data).tolist()
        else:
            return self.dataset[:n_data]

    def get_evaluation_data(self, index: int = None) -> Problem:
        """."""
        index = index or random.randint(0, len(self.dataset) - 1)
        assert index <= len(self.dataset)
        return self.dataset[index]

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
