from __future__ import annotations
"""Module.
"""
from .cell import Cell
from .balloon import Balloon
from .wind import Wind

class TargetCell(Cell):
    def __init__(self, x: int, y: int, winds: list[Wind]) -> None:
        super().__init__(x, y, winds)
        self.coverBy: set[Balloon] = set()
        self._points: int = 0

    def addBalloon(self, balloon: Balloon) -> None:
        self.coverBy.add(balloon)

    def removeBalloon(self, balloon: Balloon) -> None:
        assert balloon in self.coverBy
        self.coverBy.remove(balloon)

    def isCovered(self) -> bool:
        return len(self.coverBy)>0

    def incrPoints(self) -> None:
        self._points += 1

    def getPoints(self) -> int:
        return self._points