import sys
import os
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects.cell import Cell


class Node:
    def __init__(self, cell:Cell, alt:int, stage:int, sum:int) -> None:
        self.cell = cell
        self.alt = alt
        self.children:deque[Node] = deque()
        self.stage:int = stage
        self.points:int = len(cell.targets)
        self.sum = sum                          #excluding the current number of points
        self.ema:float = self._computeEma()     #exponential mobile average
    
    def addChild(self, node:'Node'):
        assert isinstance(node, Node)
        self.children.append(node)
    
    def resetChild(self):
        self.children = deque()
        
    def decrPointAndSum(self, amount=1):
        assert self.points-amount >= 0
        assert self.sum-amount >= 0
        self.points -= amount
        self.sum -= amount
        self.ema = self._computeEma()


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