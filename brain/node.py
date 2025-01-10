import sys
import os
from collections import deque
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from objects import Cell

class Node:
    def __init__(self, cell:Cell, alt:int, parent, presum:int, points:int) -> None:
        self.cell = cell
        self.alt = alt
        self.parent:Node|None = parent
        self.children:deque[Node] = deque()
        self.points:int = points
        self.sum = presum + points
        self.ema:float = self.computeEma()     #exponential mobile average

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
        self.ema = self.computeEma()

    def refreshSum(self, presum:int):
        """<presum> is the amount of points accumulated BEFORE this node"""
        self.sum = presum + self.points

    def computeEma(self) -> float:
        return (self.sum + self.points*3)/4

    def isLeave(self) -> bool:
        return len(self.children) == 0

    def hasParent(self) -> bool:
        return self.parent is not None

    def __repr__(self) -> str:
        return f"{self.cell}| a:{self.alt}| p:{self.points}| s:{self.sum}| e:{self.ema}"

    def __gt__(self, node:'Node') -> bool:
        return self.ema > node.ema

    def __lt__(self, node:'Node') -> bool:
        return self.ema < node.ema

    def __eq__(self, v: object) -> bool:
        return (isinstance(v, Node) 
                and self.cell == v.cell
                and self.alt == v.alt
                and self.sum == v.sum
                and self.points == v.points
                and self.ema == v.ema
                and self.children == v.children)