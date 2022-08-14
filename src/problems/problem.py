"""Data parser.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""

import zipfile
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, List


class Problem(metaclass=ABCMeta):
    """Parse the given problem.

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
        self.dataset = self._parse_data()

    @abstractmethod
    def _parse_data(self) -> List[Any]:
        """Parse data."""
        pass

    def _extract_data(self, problem: str) -> None:
        """Unzip the data file."""
        zip_path = self.data_path.with_suffix(self.ZIP_EXTENSION)
        assert Path.exists(zip_path), f"Unknown problem -> {problem}..."

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.DATA_DIR)
