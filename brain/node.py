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

    def hasParent(self) -> bool:
        return self.parent is not None

    def __repr__(self) -> str:
        return f"{self.cell}| a:{self.alt}| s:{self.sum}"

    def __gt__(self, node:'Node') -> bool:
        return self.sum > node.sum

    def __lt__(self, node:'Node') -> bool:
        return self.sum < node.sum

    def __eq__(self, v: object) -> bool:
        return (isinstance(v, Node) 
                and self.cell == v.cell
                and self.alt == v.alt
                and self.sum == v.sum
                )