"""Module.
"""
from __future__ import annotations
from .cell import Cell
from .balloon import Balloon
from .wind import Wind

class TargetCell(Cell):
    def __init__(self, x: int, y: int, winds: list[Wind]) -> None:
        """Entity that describe the wind and the target cell in range of a position by beeing a target cell"""
        super().__init__(x, y, winds)
        self.coverBy: set[Balloon] = set()
        self._points: int = 0

    def addBalloon(self, balloon: Balloon) -> None:
        """Add balloon to the target cell area"""
        self.coverBy.add(balloon)

    def removeBalloon(self, balloon: Balloon) -> None:
        """Remove balloon from the target cell area

        args:
            balloon: must be in coverBy set
        """
        assert balloon in self.coverBy
        self.coverBy.remove(balloon)

    def isCovered(self) -> bool:
        """Return if there are any balloon in the target area"""
        return len(self.coverBy)>0

    def incrPoints(self) -> None:
        self._points += 1

    def getPoints(self) -> int:
        return self._points