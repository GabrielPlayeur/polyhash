"""Module.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator
from rich.progress import track

from brain import Brain, RandomBrain, VerifyBrain
from cellMap import CellMap
from objects import Balloon
from polyparser import ParserData

@dataclass
class ResultData:
    #DONE: make a dataclass that can store ervery datas needed for generating the solution through <polysolver.stringifySolution>
    nbPoints: int
    tracking: list[list[int]]       #every balloon has its own movement

class Simulation:
    def __init__(self, parserData: ParserData) -> None:
        #Constantes
        self.ROWS: int = parserData.rows
        self.COLUMNS: int = parserData.columns
        self.ALTITUDES: int = parserData.altitudes
        self.ROUNDS: int = parserData.turns
        self.NB_BALLOONS: int = parserData.balloons

        #Variables
        self.current_round: int = 0
        self.map: CellMap = CellMap(parserData)
        self.balloons: list[Balloon] = [Balloon(self.map.startingCell) for _ in range(self.NB_BALLOONS)]
        self.brain: Brain = RandomBrain()

        #Result
        self.resultData: ResultData = ResultData(0, [ [] for _ in range(self.NB_BALLOONS)])


    def run(self) -> Iterator[tuple[int, ResultData]]:
        """Run the simulation for the given challenge, and yield the result at each turn"""
        for _ in track(range(self.ROUNDS), "Simulation in progress..."):
            self.nextTurn()
            self.current_round += 1
            
            yield self.current_round, self.resultData


    def nextTurn(self) -> None:
        coveredCells = set()
        for n, balloon in enumerate(self.balloons):
            #If the balloon is lost
            if balloon.cell is self.map.outsideCell:
                continue

            #Moving balloon
            altMoving = self.brain.solve(balloon)        #(n, self.current_round)
            balloon.moveAlt(altMoving)

            #Applying wind
            balloon.applyWind()

            #Adding movement in result
            self.resultData.tracking[n].append(altMoving)

            #Counting points
            if balloon.cell is self.map.outsideCell and balloon.alt == 0:
                continue

            for target in balloon.cell.targets:
                coveredCells.add(target)
            
        self.resultData.nbPoints += len(coveredCells)

    def result(self) -> ResultData:
        return self.resultData