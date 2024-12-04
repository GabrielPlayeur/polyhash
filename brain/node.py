import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects.cell import Cell


class Node:
    def __init__(self, cell:Cell, alt:int, stage:int, sum:int) -> None:
        self.cell = cell
        self.alt = alt
        self.children:list[Node] = []
        self.stage:int = stage
        self.points:int = len(self.cell.targets)
        self.sum = sum
    
    def addSon(self, node:'Node'):
        assert type(node) == Node
        self.children.append(node)
    
    def isLeave(self) -> bool:
        return self.children is None
    
    def __repr__(self) -> str:
        return f"{self.cell}|alt: {self.alt}|points:{self.points}"