
"""Module.
"""
from objects import Cell

class Balloon:
    def __init__(self, startCell: Cell) -> None:
        self.cell: Cell = startCell
        self.alt: int = 0
        self.altMax = len(self.cell._winds)

    def moveAlt(self, value: int) -> None:
        assert value==1 or value==0 or value==-1
        assert self.altMax > self.alt+value > 0
        self.alt += value