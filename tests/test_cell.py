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