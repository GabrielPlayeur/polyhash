
"""Module.
"""
from objects import Cell

class Balloon:
    def __init__(self, startCell: Cell) -> None:
        """Entity that describe a balloon and it's altitude"""
        self.cell: Cell = startCell
        self.alt: int = 0
        self.altMax = len(self.cell._winds)

    def moveAlt(self, value: int) -> None:
        """Change the altitude of the balloon

        args:
            value: incr, decr, don't move (1,-1,0) and must match (alt+val<=altMax) and (alt+val>0)
        """
        assert value==1 or value==0 or value==-1
        assert self.altMax >= self.alt+value > 0
        self.alt += value