"""
Module for simulating the behavior of a Cell object within a grid, with wind conditions and neighboring cells.

This module defines a Cell class that represents a cell within a grid. Each cell holds information about its position,
winds at various altitudes, neighboring cells, and target cells that may be in range. The Cell class also supports 
adding targets and neighbors, retrieving winds by altitude, and navigating between neighboring cells.
"""
from __future__ import annotations
from .wind import Wind

class Cell:
    def __init__(self, row: int, col: int, winds: list[Wind]) -> None:
        """Entity that describe the wind and the target cell in range of a position"""
        self.pos: tuple[int,int] = (row,col)
        self.row: int = row
        self.col: int = col
        self._winds: list[Wind] = winds
        self.targets: list[Cell] = []
        self.targetsSet: set[Cell] = set()
        self.neighbors: list[Cell] = []

    def addTarget(self, target: Cell) -> None:
        """Add target cell into the cell's targets list"""
        self.targets.append(target)
        self.targetsSet.add(target)

    def addNeighbor(self, cell: Cell) -> None:
        "add a neighbor at the n altitude, letting n be lenght of neighbors"
        self.neighbors.append(cell)

    def getNeighbor(self, alt: int) -> Cell:
        assert len(self._winds) > alt >= 0, f"alt: {alt}/{len(self._winds)}"
        return self.neighbors[alt]

    def getWinds(self) -> list[Wind]:
        return self._winds

    def getWindsByAlt(self, alt: int) -> Wind:
        """Get wind at the altitude

        args:
            alt: choosen altitude (0<alt<maxAlt)
        """
        assert len(self._winds) > alt >= 0
        return self._winds[alt]

    def __str__(self) -> str:
        return f"Cell ({self.row}:{self.col})"