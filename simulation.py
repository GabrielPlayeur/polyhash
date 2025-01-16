"""Module.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator

from brain import *
from cellMap import CellMap
from objects import Balloon
from polyparser import ParserData

@dataclass
class ResultData:
    #DONE: make a dataclass that can store ervery datas needed for generating the solution through <polysolver.stringifySolution>
    nbPoints: int
    tracking: list[list[int]]       #every balloon has its own movement

class Simulation:
    def __init__(self, parserData: ParserData, brain: Brain, cellMap: CellMap) -> None:
        #Constantes
        self.ROWS: int = parserData.rows
        self.COLUMNS: int = parserData.columns
        self.ALTITUDES: int = parserData.altitudes
        self.ROUNDS: int = parserData.turns
        self.NB_BALLOONS: int = parserData.balloons

        #Variables
        self.current_round: int = 0
        self.map: CellMap = cellMap
        self.balloons: list[Balloon] = [Balloon(self.map.startingCell) for _ in range(self.NB_BALLOONS)]
        self.brain: Brain = brain
        self.pointHistory = [0]

        #Result
        self.resultData: ResultData = ResultData(0, [ [] for _ in range(self.NB_BALLOONS)])

    def runIter(self) -> Iterator[tuple[int, ResultData]]:
        """Run the simulation for the given challenge, and yield the result at each turn"""
        for _ in range(self.ROUNDS):
            self.nextTurn()

            yield self.current_round, self.resultData

    def run(self) -> None:
        for _ in range(self.ROUNDS):
            self.nextTurn()

    def nextTurn(self) -> None:
        coveredCells = set()
        for n, balloon in enumerate(self.balloons):
            #If the balloon is lost
            if balloon.cell is self.map.outsideCell:
                continue
            
            #Moving balloon
            if isinstance(self.brain, VerifyBrain):
                altMoving = self.brain.solve(n, self.current_round) 
            elif isinstance(self.brain, RandomBrain):
                altMoving = self.brain.solve(balloon)
            elif isinstance(self.brain, ClosestBrain):
                altMoving = self.brain.solve(balloon, self.map.map)
            elif isinstance(self.brain, TreeBrain):
                altMoving = self.brain.solve(n, self.current_round)
            else:
                print('ERREUR this brain do not exist')
                altMoving = 0

            balloon.moveAlt(altMoving)

            #Applying wind
            balloon.applyWind()

            #Adding movement in result
            self.resultData.tracking[n].append(altMoving)

            #Counting points
            if balloon.cell is self.map.outsideCell or balloon.alt == 0:
                continue

            for target in balloon.cell.targets:
                coveredCells.add(target)
        #Add point to point history
        self.pointHistory.append(self.resultData.nbPoints)
        self.resultData.nbPoints += len(coveredCells)
        self.current_round += 1


    def prevTurn(self) -> None:
        self.current_round -= 1
        for n, balloon in enumerate(self.balloons):
            
            #Reverse apply wind and altitude
            balloon.undo(self.current_round)

            #Reverse the adding of points
            self.resultData.nbPoints = self.pointHistory[self.current_round]


    def result(self) -> ResultData:
        return self.resultData