#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module.
"""

from __future__ import annotations
from dataclasses import dataclass

from brain.brainInit import Brain
from brain.randomBrain import RandomBrain
from cellMap import CellMap
from objects import Wind, Cell, TargetCell, Balloon
from polyparser import ParserData, parseChallenge


@dataclass
class ResultData:
    #TODO: make a dataclass that can store ervery datas needed for generating the solution through <polysolver.stringifySolution>
    nbPoints:int
    tracking:list[list[int]]

class Simulation:
    def __init__(self, parserData:ParserData) -> None:
        #Constantes
        self.ROWS: int          = parserData.rows
        self.COLUMNS: int       = parserData.columns
        self.ALTITUDES: int     = parserData.altitudes
        self.ROUNDS: int        = parserData.turns
        self.NB_BALLOONS : int  = parserData.balloons

        #Variables
        self.current_round: int     = 0
        self.map: CellMap           = CellMap(parserData)
        self.balloons: set[Balloon] = set([Balloon(self.map.startingCell) for _ in range(self.NB_BALLOONS)])
        self.brain:Brain            = RandomBrain()


        #Result
        self.resultData: ResultData = ResultData(0, [])

    
    def run(self, ) -> ResultData:
        while self.current_round < self.ROUNDS:
            #TODO: write down the process of making an iteration

            self.nextTurn()

            self.current_round += 1

        return self.resultData

    def nextTurn(self) -> None:
        coveredCells = set()
        for n, balloon in enumerate(self.balloons):
            #If the balloon is lost
            if not balloon.cell:
                continue

            #Moving balloon
            altMoving = self.brain.solve(balloon)
            if altMoving:
                balloon.moveAlt(altMoving)

            #Applying wind
            balloon.applyWind()

            #Counting points
            if balloon.cell:
                for target in balloon.cell.targets:
                    coveredCells.add(target)
            
            #Adding movement in result
            if len(self.resultData.tracking) <= n:
                self.resultData.tracking.append([])
            self.resultData.tracking[n].append(altMoving)

        self.resultData.nbPoints += len(coveredCells)



if __name__ == "__main__":
    name = "a_example.in"
    name = "b_small.in"
    parser = parseChallenge(f"./challenges/{name}")
    sim = Simulation(parser)
    sim.run()
    print(sim.ROUNDS)
