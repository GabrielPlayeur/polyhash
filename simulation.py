"""Module.
"""

from __future__ import annotations
from dataclasses import dataclass

from brain import Brain, RandomBrain, VerifyBrain
from cellMap import CellMap
from objects import Wind, Cell, TargetCell, Balloon
from polyparser import ParserData

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
        self.brain: Brain = RandomBrain()
        # self.brain: Brain = VerifyBrain("output/c_medium_143(152).txt")

        #Result
        self.resultData: ResultData = ResultData(0, [ [] for _ in range(self.NB_BALLOONS)])

    def run(self) -> ResultData:
        for _ in range(self.ROUNDS):
            self.nextTurn()
        return self.resultData

    def nextTurn(self) -> None:
        coveredCells = set()
        for n, balloon in enumerate(self.balloons):
            #If the balloon is lost
            if balloon.cell is self.map.outsideCell:
                continue

            #Moving balloon
            altMoving = self.brain.solve(balloon)
            # altMoving = self.brain.solve(n, self.current_round)
            balloon.moveAlt(altMoving)

            #Applying wind
            balloon.applyWind()

            #Adding movement in result
            self.resultData.tracking[n].append(altMoving)

            #Counting points
            if balloon.cell is self.map.outsideCell:
                continue

            for target in balloon.cell.targets:
                coveredCells.add(target)

        self.resultData.nbPoints += len(coveredCells)
        self.current_round += 1