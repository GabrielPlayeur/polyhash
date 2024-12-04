"""Module.
"""

from __future__ import annotations
from dataclasses import dataclass

from brain import Brain, RandomBrain, VerifyBrain
from cellMap import CellMap
from objects import Wind, Cell, TargetCell, Balloon
from polyparser import ParserData, parseChallenge
#from rich.progress import track

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
        self.pointHistory = []

        #Result
        self.resultData: ResultData = ResultData(0, [ [] for _ in range(self.NB_BALLOONS)])

    def run(self) -> ResultData:
        for _ in track(range(self.ROUNDS), "Simulation in progress..."):
            #TODO: write down the process of making an iteration

            self.nextTurn()

        return self.resultData

    def nextTurn(self) -> None:
        coveredTargets = set()
        for n, balloon in enumerate(self.balloons):
            #If the balloon is lost
            if balloon.cell is self.map.outsideCell:
                continue
            
            #Add state to history

            balloon.appendHistory(self.current_round, balloon.alt)

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
                coveredTargets.add(target)

        #Add point to point history
        self.pointHistory.append(self.resultData.nbPoints)
            
        self.resultData.nbPoints += len(coveredTargets)

        self.current_round += 1


    def prevTurn(self) -> None:
        for n, balloon in enumerate(self.balloons):
            self.current_round -= 1
            
            #Reverse apply wind and altitude
            balloon.undo(self.current_round)

            #Reverse the adding of points
            self.resultData.nbPoints = self.pointHistory[self.current_round]

            

            