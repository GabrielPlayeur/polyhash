import pytest

from cellMap import CellMap
from objects.targetCell import TargetCell
from polyparser import parseChallenge


def test_cellMap_init():
    challenges = ["a_example", "b_small", "c_medium", "d_final"]
    for challenge in challenges:
        parser = parseChallenge(f"./challenges/{challenge}.in")
        cellMap = CellMap(parser)

        assert len(cellMap.map) == parser.rows and len(cellMap.map[0]) == parser.columns, f"Failed to create the map of the challenge {challenge}"
        
        assert parser.starting_cell == cellMap.startingCell.pos, f"the starting cell is not at the right position"
        
        for row, col in parser.targets_pos:
            assert len(cellMap.map) >= row and len(cellMap.map[row]) >= col
            assert type(cellMap.map[row][col]) is TargetCell, f"The cell {row}:{col} should be a target"
            assert len(cellMap.map[row][col]._winds) == parser.altitudes, f"The cell {row}:{col} has not enough layer of wind"

            #wind test
            for alt in range(len(parser.winds[row][col])):
                assert parser.winds[row][col][alt] == cellMap.map[row][col].getWinds(alt+1).vec, f"the wind is wrong at the altitude {alt+1}"



        


