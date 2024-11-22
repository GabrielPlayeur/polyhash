#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module.
"""

from __future__ import annotations
from cells import Cell, TargetCell
from wind import Wind
from polyparser import ParserData, parseChallenge

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
            for col in range(self.columns):

                winds = []
                for vec in parserData.winds:
                    winds.append(Wind(vec[0], vec[1]))

                if (row, col) in parserData.targets_pos:
                    cell = TargetCell(row, col, tuple(winds))
                else:
                    cell = Cell(row, col, tuple(winds))

                if (cell.x, cell.y) == parserData.starting_cell:
                    self.startingCell = cell

                self.map.append(cell)

    
    def defineTargetRange(self, parserData: ParserData) -> None: #test pas fait !!
        """Defini les cellules en périhérie d'une target"""
        for targetPos in parserData.targets_pos:
            target = self.map[targetPos.y][targetPos.x]
            for row in range(target.x-self.radius, target.x+self.radius+1):
                for col in range(target.y-self.radius, target.y+self.radius+1):
                    cell:Cell = self.map[row][col]
                    if self.inRange(target, cell):
                        cell.addTarget(target)
                
            
            

    def inRange(self, target:TargetCell, cell:Cell) -> bool:
        """Retourne si la cellule est dans le rayon <self.radius> de target"""
        columndist = lambda c1, c2: min(abs(c1-c2), self.columns - abs(c1-c2))
        return (cell.x - target.x)**2 + columndist(cell.y, target.y)**2 <= self.radius
    
    def print(self, altitude:int):  #pour l'instant affiche les celulles et les targets
        """Affiche la carte des vents à l'altitude donnée"""

        assert 0 < altitude < self.altitudes, f"L'altitude {altitude} n'existe pas"

        print(f"Affichage de la carte de taille {self.rows}x{self.columns}\n\n")
        for row in range(self.rows):
            for col in range(self.columns):
                cell:Cell = self.map[row][col]
                if cell.pos == self.startingCell:
                    print("s", end="")
                elif type(cell) == TargetCell:
                    print("T", end="")
                elif len(cell.targets) > 0:
                    print("P", end="")
                else:
                    print("_", end="")
            print("\n")

    
    def save(fileName:str):
        ...
    
    def load(fileName:str) -> CellMap:
        ...


if __name__ == "__main__":
    cellMap = CellMap(parseChallenge("/challenges/a_example.in"))
    cellMap.print()


