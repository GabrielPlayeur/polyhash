import pytest
from objects import Cell
from objects.wind import Wind

class TestCell:

    def test_cell_init(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = Cell(row,col,winds)
        assert type(cell) == Cell
        assert cell.row==row and cell.col==col and cell.pos==(row,col)
        assert len(cell._winds)==2

    def test_cell_addTarget(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = Cell(row,col,winds)
        target = Cell(0,0,winds)
        cell.addTarget(target)
        assert len(cell.targets)==1
        assert cell.targets[0] is target

    def test_cell_getWindsByAlt(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = Cell(row,col,winds)
        assert cell.getWindsByAlt(1)==winds[1]
        assert cell.getWindsByAlt(0)==winds[0]
        with pytest.raises(AssertionError):
            cell.getWindsByAlt(-1)
        with pytest.raises(AssertionError):
            cell.getWindsByAlt(2)

    def test_cell_getNeighbor(self):
        winds = [Wind(0, 0), Wind(1, 0), Wind(3, 0)]
        cell = Cell(0, 0, winds)
        n = Cell(10, 1, winds)
        cell.neighbors = [cell, Cell(0, 1, winds), n]

        with pytest.raises(AssertionError):
            cell.getNeighbor(-1)
            
        with pytest.raises(AssertionError):
            cell.getNeighbor(3)
            
        assert cell.getNeighbor(0) == cell
        assert cell.getNeighbor(1) == cell.neighbors[1]
        assert cell.getNeighbor(2) == n
        