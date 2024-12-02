"""Module.
"""

from __future__ import annotations
from dataclasses import dataclass

from brain import Brain, RandomBrain, VerifyBrain
from cellMap import CellMap
from objects import Wind, Cell, TargetCell, Balloon
from polyparser import ParserData, parseChallenge
from rich.progress import track

@dataclass
class ResultData:
    #TODO: make a dataclass that can store ervery datas needed for generating the solution through <polysolver.stringifySolution>
    nbPoints: int
    tracking: list[list[int]]

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
        self.brain: Brain = VerifyBrain()

        #Result
        self.resultData: ResultData = ResultData(0, [ [] for _ in range(self.NB_BALLOONS)])

    def run(self) -> ResultData:
        for _ in track(range(self.ROUNDS), "Simulation in progress..."):
            #TODO: write down the process of making an iteration

            self.nextTurn()

            self.current_round += 1

        return self.resultData

    def nextTurn(self) -> None:
        coveredCells = set()
        for n, balloon in enumerate(self.balloons):
            #If the balloon is lost
            if balloon.cell is self.map.outsideCell:
                continue

            #Moving balloon
            altMoving = self.brain.solve(n, self.current_round)
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