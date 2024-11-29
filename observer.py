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

class Observer:
    """This observer will check the consistency between the giving result and the re-computed one"""
    def __init__(self, parserData:ParserData) -> None:
        self.balloonPositions: list[XYZ] = []
        self.parser: ParserData          = parserData

    def _updateBalloonPosition(self, indexBalloon, move) -> None:
        """Re-computing the simulation"""
        xyz = self.balloonPositions[indexBalloon]
        assert xyz.row != -1

        #moving the balloon
        xyz.alt =+ self._checkAlt(xyz.alt, move)

        #applying the wind
        dRow, dCol = self.parser.winds[xyz.row][xyz.col][xyz.alt]
        xyz.row = xyz+dRow if 0 <= xyz+dRow < self.parser.rows else -1
        xyz.col = (xyz.col + dCol)%self.parser.columns


    def _checkAlt(self, alt:int, move:int) -> int:
        """Avoid limit case in altitude"""
        return move if (alt == 0 and move != -1) or (0 < alt+move <= self.parser.altitudes) else 0
            


    def inspect(self, partial:ResultData) -> bool:
        """Checks partial data given as input"""

        return False