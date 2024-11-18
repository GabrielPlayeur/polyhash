
"""Module.
"""
from cell import Cell
from balloons import Balloon
from __future__ import annotations

class TargetCell(Cell):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.coverBy: set[Balloon]
        # self.targets: tuple[TargetCell] # (self)
        self.points: int

    def addBalloon(self, balloon: Balloon) -> None:
        raise NotImplementedError

    def removeBalloon(self, balloon: Balloon) -> None:
        raise NotImplementedError

    # def addTarget(self, target: TargetCell) -> None:
    #     raise NotImplementedError

    def incrPoints(self) -> None:
        raise NotImplementedError