import sys
import os
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects.cell import Cell


class Node:
    def __init__(self, cell:Cell, alt:int, stage:int, sum:int, points:int) -> None:
        self.cell = cell
        self.alt = alt
        self.children:deque[Node] = deque()
        self.stage:int = stage
        self.points:int = points
        self.sum = sum                          #excluding the current number of points
        self.ema:float = self._computeEma()     #exponential mobile average
    
    def addChild(self, node:'Node'):
        assert type(node) == Node
        self.children.append(node)
    
    def isLeave(self) -> bool:
        return len(self.children) == 0
    
    def __repr__(self) -> str:
        return f"{self.cell}|alt: {self.alt}|points:{self.points}"
    
    def _computeEma(self) -> float:
        return (self.sum + self.points*3)/4
    
    def __gt__(self, node:'Node') -> bool:
        return self.ema > node.ema
    
    def __lt__(self, node:'Node') -> bool:
        return self.ema < node.ema