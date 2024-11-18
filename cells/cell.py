
"""Module.
"""
from wind import Wind
from __future__ import annotations

class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.pos: tuple[int,int] # (0,0)
        self.x: int
        self.y: int
        self._winds: tuple[Wind] # ((1,0), (-1,0), (0,3))
        self.targets: tuple[Cell]

    def addTarget(self, target: Cell) -> None:
        raise NotImplementedError

    def addWind(self, wind: int) -> None:
        raise NotImplementedError

    def setWinds(self, winds: list[int]) -> None:
        raise NotImplementedError

    def getWinds(self, alt: int) -> Wind:
        raise NotImplementedError