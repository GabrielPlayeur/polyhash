import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects import Cell

class Node:
    def __init__(self, cell:Cell, alt:int, parent, sum:int) -> None:
        self.cell = cell
        self.alt = alt
        self.parent:Node|None = parent
        self.sum = sum

    def __lt__(self, node:'Node') -> bool:
        return self.sum < node.sum