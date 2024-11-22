from __future__ import annotations
"""Module.
"""
from .wind import Wind

class Cell:
    def __init__(self, x: int, y: int, winds: list[Wind]) -> None:
        self.pos: tuple[int,int] = (x,y)
        self.x: int = x
        self.y: int = y
        self._winds: list[Wind] = winds
        self.targets: list[Cell] = []

    def addTarget(self, target: Cell) -> None:
        self.targets.append(target)

    def getWinds(self, alt: int) -> Wind:
        assert len(self._winds)+1 > alt > 0
        return self._winds[alt-1]
    
    def __str__(self) -> str:
        return f"Cell ({self.x}:{self.y})"