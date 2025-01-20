from __future__ import annotations
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects import Cell

class Node:
    """A class representing a node in the pathfinding algorithm.

    This class is used to store information about a position in the grid, including its
    associated cell, altitude, parent node, and cumulative cost.
    """

    def __init__(self, cell: Cell, alt: int, parent: Node | None, sum: int) -> None:
        self.cell = cell
        self.alt = alt
        self.parent = parent
        self.sum = sum

    def __lt__(self, node: Node) -> bool:
        return self.sum < node.sum