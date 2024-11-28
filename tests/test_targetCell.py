import pytest
from objects import TargetCell, Wind, Balloon

class TestTargetCell:

    def test_targetCell_init(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = TargetCell(row,col,winds)
        assert type(cell) == TargetCell
        assert len(cell.coverBy)==0
        assert cell._points==0

    def test_targetCell_addBalloon(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = TargetCell(row,col,winds)
        balloon = Balloon(cell)
        cell.addBalloon(balloon)
        assert balloon in cell.coverBy and len(cell.coverBy)==1

    def test_targetCell_delBalloon(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = TargetCell(row,col,winds)
        balloon = Balloon(cell)
        cell.addBalloon(balloon)
        cell.removeBalloon(balloon)
        assert len(cell.coverBy)==0
        with pytest.raises(AssertionError):
            cell.removeBalloon(balloon)

    def test_targetCell_isCovered(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = TargetCell(row,col,winds)
        assert cell.isCovered()==False
        balloon = Balloon(cell)
        cell.addBalloon(balloon)
        assert cell.isCovered()==True
        cell.removeBalloon(balloon)
        assert cell.isCovered()==False

    def test_targetCell_incrPoints(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = TargetCell(row,col,winds)
        assert cell._points==0
        cell.incrPoints()
        assert cell._points==1

    def test_targetCell_getPoints(self):
        row,col = 0,0
        winds = [Wind(0,0),Wind(0,0)]
        cell = TargetCell(row,col,winds)
        assert cell.getPoints()==0
        cell.incrPoints()
        assert cell.getPoints()==1