"""Problem solver.

Author:
    - Name: Wooshik Myung
    - Email: wooshik.m@gmail.com
"""

from abc import ABCMeta, abstractmethod
from typing import Any


class Solver(metaclass=ABCMeta):
    """Abstract class of the solver."""

    def __init__(self, **_: Any) -> None:
        """Initialize."""
        pass

    @abstractmethod
    def __call__(self) -> None:
        """."""
        pass

    @abstractmethod
    def _optimize(self) -> None:
        """."""
        pass
