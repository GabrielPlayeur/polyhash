"""
Module for simulating the behavior of a Balloon object within a cellular grid environment.

This module defines a Balloon class that represents a balloon's movement and interaction with winds at different altitudes.
The Balloon can change its altitude, apply wind effects, and undo movements, tracking its history across various cells.
"""
from objects import Cell

class Balloon:
    def __init__(self, startCell: Cell) -> None:
        """Entity that describe a balloon and it's altitude"""
        self.cell: Cell = startCell
        self.cellHistory: list[tuple[(Cell,int)]] = [(startCell, 0)] #Cell -> previous Cell, int -> previous altitude
        self.alt: int = 0
        self.altMax: int = len(self.cell._winds)-1

    def moveAlt(self, value: int) -> None:
        """Change the altitude of the balloon

        args:
            value: incr, decr, don't move (1,-1,0) and must match (alt+val<=altMax) and (alt+val>0)
        """
        if self.alt==0 and value==0: return
        assert value==1 or value==0 or value==-1
        assert self.altMax >= self.alt+value > 0, f"alt is not good (alt: {self.alt+value})"
        self.alt += value

    def applyWind(self) -> None:
        """Apply the wind at the current altitude"""
        for target in self.cell.targets:
            if self in target.coverBy: # type: ignore
                target.coverBy.remove(self) # type: ignore
        self.cell = self.cell.getNeighbor(self.alt)
        for target in self.cell.targets:
            target.coverBy.add(self) # type: ignore
        self.cellHistory.append((self.cell,self.alt))

    def undo(self, numberTurn):
        self.cell = self.cellHistory[numberTurn][0]
        self.alt = self.cellHistory[numberTurn][1]
        self.cellHistory = self.cellHistory[:numberTurn+1]