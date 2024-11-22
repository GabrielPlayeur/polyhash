#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module.
"""

from cells import Cell, TargetCell
from wind import Wind
from __future__ import annotations

class CellMap:
    """ Cette class représente la carte des vents sous forme d'un graph de Cells.
        \n\t
    """

    def __init__(self, parserData:ParserData) -> None:
        self.rows:int = parserData.rows
        self.columns:int = parserData.columns
        self.altitudes:int = parserData.altitudes
        self.startingCell:Cell
        self.turns = parserData.turns
        self.ballons = parserData.balloons
        self.radius = parserData.radius

        self.map:list[Cell] = [[],]
        
        self.initialize(parserData)
        self.defineTargetRange(parserData)

            
    def initialize(self, parserData:ParserData) -> None:
        """Initialisation de la matrice de cellule"""

        for row in range(self.rows):
            for col in range(self.cols):

                winds = []
                for vec in parserData.winds:
                    winds.append(Wind(vec[0], vec[1]))

                if (row, col) in parserData.targets_pos:
                    curCell = TargetCell(row, col, tuple(winds))
                else:
                    curCell = Cell(row, col, tuple(winds))

                if (curCell.x, curCell.y) == parserData.starting_cell:
                    self.startingCell = curCell

                self.map.append(curCell)

    
    def defineTargetRange(self, parserData: ParserData) -> None:
        """Defini les cellules en périhérie d'une target"""
        for targetPos in parserData.targets_pos:
            target = self.map[targetPos.y][targetPos.x]
            for row in range(target.y-self.radius, target.y+self.radius+1):
                for col in range(target.y-self.radius, target.y+self.radius+1):
                    curCell:Cell = self.map[row][col]
                    if self.inRange(target, curCell):
                        curCell.addTarget(target)
                
            
            

    def inRange(self, target:TargetCell, cell:Cell) -> bool:
        columndist = lambda c1, c2: min(abs(c1-c2), self.columns - abs(c1-c2))
        return (cell.x - target.x)**2 + columndist(cell.y, target.y)**2 <= self.radius


    
    def save(fileName:str):
        ...
    
    def load(fileName:str) -> CellMap:
        ...
