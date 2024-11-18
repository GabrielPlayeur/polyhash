
"""Module.
"""
from cell import Cell
from targetCell import TargetCell

class ZoneCell(Cell):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.targets: tuple[TargetCell] # (TargetCell)

    def addTarget(self, target: TargetCell) -> None:
        raise NotImplementedError