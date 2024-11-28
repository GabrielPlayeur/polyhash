#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module.
"""

from __future__ import annotations
from dataclasses import dataclass

from brain.brainInit import Brain
from cellMap import CellMap
from objects import Wind, Cell, TargetCell, Balloon
from polyparser import ParserData, parseChallenge


@dataclass
class ResultData:
    #TODO: make a dataclass that can store ervery datas needed for generating the solution through <polysolver.stringifySolution>
    ...

class Simulation:
    def __init__(self, parserData:ParserData) -> None:
        #Constantes
        self.ROWS: int       = parserData.rows
        self.COLUMNS: int    = parserData.columns
        self.ALTITUDES: int  = parserData.altitudes
        self.ROUNDS: int     = parserData.turns
        self.BALLOONS : int  = parserData.balloons

        #Variables
        self.current_round: int     = parserData.rows
        self.map: CellMap  = CellMap(parserData)
        self.balloons: set[Balloon]
        self.brain:Brain

    
    def run(self, ) -> ResultData:
        while self.current_round < self.ROUNDS:
            #TODO: write down the process of making an iteration

            self.nextTurn()
            
            self.current_round += 1

        return ResultData()

    def nextTurn(self) -> None:
        for balloon in self.balloons:

            #Moving balloon
            altMoving = self.brain.solve()
            balloon.moveAlt(altMoving)

            #Applying wind
            self.applyWind(balloon)

            #Counting points
            self.countPoints(balloon.cell)


    def applyWind(self, balloon) -> None:
        #TODO: this method should be moving one or every balloon under the wind of the cell they are on
        ...

    def countPoints(self, cell) -> int:
        #TODO: write it
        return 0

