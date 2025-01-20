"""Module containing the abstract class Brain.

This module defines an abstract base class (ABC) named `Brain`, which serves as a template for subclasses that implement a `solve` method.
"""

from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects import *

class Brain(ABC):
    """Abstract base class representing a problem-solving entity.

    This class defines an interface for solving problems by enforcing the implementation 
    of the `solve` method in any subclass.
    """

    @abstractmethod
    def solve(self, *args, **kwargs) -> int:
        """Abstract method to solve a given problem.

        This method must be implemented by subclasses to define specific problem-solving logic.

        Returns:
            int: The result of the problem-solving process.
        """
        ...