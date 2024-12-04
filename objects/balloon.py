
"""Module.
"""
from objects import Cell

class Balloon:
    def __init__(self, startCell: Cell) -> None:
        """Entity that describe a balloon and it's altitude"""
        self.cell: Cell = startCell
        self.cellHistory: list[tuple[(Cell,int)]] = [] #Cell -> previous Cell, int -> previous altitude
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
            assert isinstance(target, TargetCell)
            target.coverBy.remove(self)

        self.cell = self.cell.getNeighbor(self.alt)

        for target in self.cell.targets:
            target.coverBy.add(self)


    def appendHistory(self, numberTurn, newAlt):
        assert numberTurn <= len(self.cellHistory)
        if numberTurn < len(self.cellHistory): 
            '''
            In case we're in the past we overwrite the future state since
            apart from the random strategy every strategy is determinist
            '''
            self.cellHistory = self.cellHistory[:numberTurn]
        self.cellHistory.append((self.cell,newAlt))

    
    def undo(self, numberTurn):
        self.cell = self.cellHistory[numberTurn][0]
        self.alt = self.cellHistory[numberTurn][1]



