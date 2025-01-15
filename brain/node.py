from __future__ import annotations
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects import Cell

#TODO: add doc
class Node:
    def __init__(self, cell: Cell, alt: int, parent: Node|None, sum: int) -> None:
        self.cell = cell
        self.alt = alt
        self.parent = parent
        self.sum = sum

    def __lt__(self, node: Node ) -> bool:
        return self.sum < node.sum