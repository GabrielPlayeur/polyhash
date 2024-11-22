import pytest
from objects import Cell
from wind import Wind

class TestCell:

    def test_cell_init(self):
        x,y = 0,0
        winds = [Wind(0,0)]
        cell = Cell(x,y,winds)
        assert type(cell) == Cell
        assert cell.x==x and cell.y==y and cell.pos==(x,y)
        assert len(cell._winds)==1

    def test_cell_addTarget(self):
        x,y = 0,0
        winds = [Wind(0,0)]
        cell = Cell(x,y,winds)
        target = Cell(0,0,winds)
        cell.addTarget(target)
        assert len(cell.targets)==1
        assert cell.targets[0] is target

    def test_cell_getWinds(self):
        x,y = 0,0
        winds = [Wind(0,0)]
        cell = Cell(x,y,winds)
        assert cell.getWinds(1)==winds[0]
        with pytest.raises(AssertionError):
            cell.getWinds(0)
        with pytest.raises(AssertionError):
            cell.getWinds(2)
