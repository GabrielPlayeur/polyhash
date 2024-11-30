"""Module.
"""

from __future__ import annotations
from dataclasses import dataclass
from simulation import ResultData
from polyparser import ParserData

@dataclass
class XYZ:
    """Easy coordinate system (row, col, alt)"""
    row: int
    col: int
    alt: int

    def __hash__(self) -> int:
        return hash((self.row, self.col, self.alt))



class Observer:
    """This observer will check the consistency between the giving result and the re-computed one"""

    def __init__(self, parserData:ParserData) -> None:
        self.parser: ParserData = parserData
        self.balloonPositions: list[XYZ] = []
        self.nbPoints = 0
        self.fileName:str


    def _simulatingBalloonMove(self, indexBalloon:int, move:int) -> set[XYZ]:
        """Re-computing the simulation"""
        balloon = self.balloonPositions[indexBalloon]

        if balloon.row == -1 or balloon.alt == 0 and move == 0:
            return set()

        #moving the balloon
        balloon.alt += self._checkAlt(balloon.alt, move)


        #applying the wind
        dRow, dCol = self.parser.winds[balloon.row][balloon.col][balloon.alt]
        balloon.row = balloon.row+dRow if 0 <= balloon.row+dRow < self.parser.rows else -1
        balloon.col = (balloon.col + dCol)%self.parser.columns


        #finding target covered
        return self._targetInRange(balloon)


    def _checkAlt(self, alt:int, move:int) -> int:
        """Avoid limit case in altitude"""
        return move if (alt == 0 and move != -1) or (0 < alt+move <= self.parser.altitudes) else 0


    def _targetInRange(self, balloon:XYZ) -> set[XYZ]:
        """Find all target in range of this balloon"""
        targetInRange = set()
        for row, col in self.parser.targets_pos:
            target = XYZ(row, col, -1)
            if self._inRange(balloon, target):
                targetInRange.add(target)
        
        return targetInRange
    

    def _inRange(self, balloon: XYZ, cell: XYZ) -> bool:
        """Same function in CellMap, return true whenever the cell is in the radius of the balloon"""
        columndist = lambda c1, c2: min(abs(c1-c2), self.parser.columns - abs(c1-c2))
        return (cell.row - balloon.row)**2 + columndist(cell.col, balloon.col)**2 <= self.parser.radius**2
    

    def _init(self, partial:ResultData):
        #managing logs
        with open(self.fileName, "w") as f: #ersing precedents logs if exist
            f.write("")
        output = "\n\n__OBSERVER's_REPORT____________________________\n"
        self._log(output)


        #initializing variables
        for _ in partial.tracking:
            row, col = self.parser.starting_cell
            self.balloonPositions.append(XYZ(row, col, 0))
    
    def _log(self, output):
        allowed = hasattr(self, "fileName")
        if allowed and self.fileName != "-1":
            with open(self.fileName, "a") as f:
                print(output, file=f)
        elif not allowed:
            print(output)
    
    def generateLog(self, fileName:str):
        assert fileName[-4:] == ".log", "not the right extension: .log"
        self.fileName = fileName
    
    def noLog(self):
        self.fileName = "-1"


    def inspect(self, turn:int, partial:ResultData) -> bool:
        """Checks partial data given as input at the n-th turn"""

        turn -= 1
        
        if not self.balloonPositions:
            self._init(partial)
        
        allTargetCovered, i = set(), 0
        for index, balloonPath in enumerate(partial.tracking):
            if len(balloonPath) == turn+1:
                targetCovered = self._simulatingBalloonMove(index, balloonPath[turn])
                allTargetCovered.update(targetCovered)
                i+=1
                

        self.nbPoints += len(allTargetCovered)
        self._log(f"""Inspection at {turn}-th turn:
        -Simulated count of point: {partial.nbPoints} \t\t\t\t -Given tracking result: {partial.tracking}
        -Checked count of point: {self.nbPoints} \t\t\t\t -Recomputed balloon position: {[b for b in self.balloonPositions]}
        -Nb of balloon updated: {i} \t\t\t\t -Nb of balloon untracked: {len(partial.tracking)-i}
        \n""")
        return self.nbPoints == partial.nbPoints