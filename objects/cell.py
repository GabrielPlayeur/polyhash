"""Module.
"""
from __future__ import annotations
from .wind import Wind

class Cell:
    def __init__(self, row: int, col: int, winds: tuple[Wind]) -> None:
        """Entity that describe the wind and the target cell in range of a position"""
        self.pos: tuple[int,int]          = (row,col)
        self.row: int = row
        self.col: int = col
        self._winds: tuple[Wind]          = winds
        self.targets: list[Cell]          = []
        self.neighbors: list[Cell|None]   = []

    def addTarget(self, target: Cell) -> None:
        """Add target cell into the cell's targets list"""
        self.targets.append(target)

    def addNeighbor(self, cell:Cell|None) -> None:
        "add a neighbor at the n+1 altitude, letting n be lenght of neighbors"
        self.neighbors.append(cell)

    def getWinds(self, alt: int) -> Wind:
        """Get wind at the altitude

        args:
            alt: choosen altitude (0<alt<maxAlt)
        """
        assert len(self._winds)+1 > alt > 0
        return self._winds[alt-1]
    
    def __str__(self) -> str:
        return f"Cell ({self.row}:{self.col})"