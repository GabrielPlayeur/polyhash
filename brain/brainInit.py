from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects import *

class Brain(ABC):
    @abstractmethod
    def solve(self, *args, **kwargs) -> int:
        ...