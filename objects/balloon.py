
"""Module.
"""
from objects import Cell

class Balloon:
    def __init__(self, startCell: Cell) -> None:
        """Entity that describe a balloon and it's altitude"""
        self.cell: Cell = startCell
        self.cellHistory: list[tuple[(Cell,int)]] = [(startCell, 0)] #Cell -> previous Cell, int -> previous altitude
        self.alt: int = 0
        self.altMax = len(self.cell._winds)-1

    def moveAlt(self, value: int) -> None:
        """Change the altitude of the balloon

        args:
            value: incr, decr, don't move (1,-1,0) and must match (alt+val<=altMax) and (alt+val>0)
        """
        if self.alt==0 and value==0: return
        assert value==1 or value==0 or value==-1
        assert self.altMax >= self.alt+value > 0
        self.alt += value

    def applyWind(self) -> None:
        """Apply the wind at the current altitude"""
        for target in self.cell.targets:
            if self in target.coverBy:
                target.coverBy.remove(self)
        self.cell = self.cell.getNeighbor(self.alt)

        for target in self.cell.targets:
            target.coverBy.add(self)
        self.cellHistory.append((self.cell,self.alt))
    
    def undo(self, numberTurn):
        self.cell = self.cellHistory[numberTurn][0]
        self.alt = self.cellHistory[numberTurn][1]
        self.cellHistory = self.cellHistory[:numberTurn+1]