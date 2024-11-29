import pytest

from cellMap import CellMap
from objects import TargetCell,Cell
from polyparser import parseChallenge


class TestCellMap:
    def test_cellMap_init(self):
        challenges = ["a_example", "b_small", "c_medium", "d_final"]
        for challenge in challenges:
            parser = parseChallenge(f"./challenges/{challenge}.in")
            cellMap = CellMap(parser)
            assert len(cellMap.map) == parser.rows and len(cellMap.map[0]) == parser.columns, f"Failed to create the map of the challenge {challenge}"
            assert parser.starting_cell == cellMap.startingCell.pos, f"the starting cell is not at the right position"
            for row, col in parser.targets_pos:
                assert len(cellMap.map) >= row and len(cellMap.map[row]) >= col
                assert type(cellMap.map[row][col]) is TargetCell, f"The cell {row}:{col} should be a target"
                assert len(cellMap.map[row][col]._winds) == parser.altitudes+1, f"The cell {row}:{col} has not enough layer of wind"
                for alt in range(len(parser.winds[row][col])):
                    assert parser.winds[row][col][alt] == cellMap.map[row][col].getWindsByAlt(alt).vec, f"the wind is wrong at the altitude {alt+1}"


    def test_cellMap_inRange(self, ):
        parser = parseChallenge(f"./challenges/a_example.in")
        mapCell = CellMap(parser)

        assert mapCell.inRange(mapCell.map[0][1], mapCell.map[0][0]) == True
        assert mapCell.inRange(mapCell.map[0][1], mapCell.map[0][3]) == False
        assert mapCell.inRange(mapCell.map[0][1], mapCell.map[1][0]) == False
        assert mapCell.inRange(mapCell.map[0][0], mapCell.map[0][4]) == True
        assert mapCell.inRange(mapCell.map[0][1], mapCell.map[0][0]) == True
        assert mapCell.inRange(mapCell.map[0][1], mapCell.map[0][3]) == False
        assert mapCell.inRange(mapCell.map[0][1], mapCell.map[1][0]) == False
        assert mapCell.inRange(mapCell.map[0][0], mapCell.map[0][4]) == True

        mapCell.radius = 2

        listTest = [(0, 0), (0,1), (0,3), (0,4), (1,1), (1,2), (1,3), (2, 2)]
        for row, col in listTest:
            assert mapCell.inRange(mapCell.map[0][2], mapCell.map[row][col]) == True

        listTest = [(1, 0), (1,4), (2,0), (2,1), (2,3), (2,4)]
        for row, col in listTest:
            assert mapCell.inRange(mapCell.map[0][2], mapCell.map[row][col]) == False


    def test_cellMap_getCell(self, ):
        parser = parseChallenge(f"./challenges/a_example.in")
        mapCell = CellMap(parser)

        with pytest.raises(AssertionError):
            mapCell.getCell(-1, 3)
        with pytest.raises(AssertionError):
            mapCell.getCell(-1, 3)

        with pytest.raises(AssertionError):
            mapCell.getCell(mapCell.rows, 3)
        with pytest.raises(AssertionError):
            mapCell.getCell(mapCell.rows, 3)

        with pytest.raises(AssertionError):
            mapCell.getCell(1, -1)
        with pytest.raises(AssertionError):
            mapCell.getCell(1, -1)

        with pytest.raises(AssertionError):
            mapCell.getCell(mapCell.rows, mapCell.columns)
        with pytest.raises(AssertionError):
            mapCell.getCell(mapCell.rows, mapCell.columns)

        assert mapCell.getCell(1, 2) == mapCell.map[1][2]

    def test_cellMap_createGraph(self):
        parser = parseChallenge(f"./challenges/a_example.in")
        mapCell = CellMap(parser)
        print(mapCell)
        neighborMapAlt1 = [[ mapCell.map[0][1], mapCell.map[0][2], mapCell.map[0][3], mapCell.map[0][4], mapCell.map[0][0]],
                           [ mapCell.map[1][1], mapCell.map[1][2], mapCell.map[1][3], mapCell.map[1][4], mapCell.map[1][0]],
                           [ mapCell.map[2][1], mapCell.map[2][2], mapCell.map[2][3], mapCell.map[2][4], mapCell.map[2][0]]
        ]
        neighborMapAlt2 = [[ mapCell.outsideCell, mapCell.outsideCell, mapCell.outsideCell, mapCell.outsideCell, mapCell.outsideCell],
                           [ mapCell.map[0][0], mapCell.map[0][1], mapCell.map[0][2], mapCell.map[0][3], mapCell.map[0][4]],
                           [ mapCell.map[1][0], mapCell.map[1][1], mapCell.map[1][2], mapCell.map[1][3], mapCell.map[1][4]]
        ]
        neighborMapAlt3 = [[ mapCell.map[0][1], mapCell.map[0][2], mapCell.map[0][3], mapCell.map[0][0], mapCell.map[0][0]],
                           [ mapCell.map[1][2], mapCell.map[1][2], mapCell.map[1][4], mapCell.map[1][1], mapCell.map[1][1]],
                           [ mapCell.map[2][1], mapCell.map[2][2], mapCell.map[2][3], mapCell.map[2][0], mapCell.map[2][0]]
        ]
        for row in range(parser.rows):
            for col in range(parser.columns):
                assert mapCell.map[row][col].getNeighbor(0) == mapCell.map[row][col]
                assert mapCell.map[row][col].getNeighbor(1) == neighborMapAlt1[row][col]
                assert mapCell.map[row][col].getNeighbor(2)== neighborMapAlt2[row][col]
                assert mapCell.map[row][col].getNeighbor(3) == neighborMapAlt3[row][col]