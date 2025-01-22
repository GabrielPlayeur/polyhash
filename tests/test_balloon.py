import pytest
from objects import Cell, Wind, Balloon, TargetCell

class TestBalloon:

    def test_balloon_init(self):
        cell = Cell(0,0,[Wind(0,0),Wind(0,0),Wind(0,0)])
        balloon = Balloon(cell)
        assert type(balloon) == Balloon
        assert balloon.alt==0
        assert balloon.altMax==2

    def test_balloon_moveAlt(self):
        cell = Cell(0,0,[Wind(0,0),Wind(0,0),Wind(0,0)])
        balloon = Balloon(cell)
        balloon.moveAlt(0)
        balloon.moveAlt(1)
        assert balloon.alt==1
        balloon.moveAlt(0)
        assert balloon.alt==1
        balloon.moveAlt(1)
        assert balloon.alt==2
        with pytest.raises(AssertionError):
            balloon.moveAlt(1)
        balloon.moveAlt(-1)
        assert balloon.alt==1
        with pytest.raises(AssertionError):
            balloon.moveAlt(-1)
        with pytest.raises(AssertionError):
            balloon.moveAlt(10)
        with pytest.raises(AssertionError):
            balloon.moveAlt(-10)

    def test_balloon_applyWind(self):
        cellStart = Cell(0,0,[Wind(0,0),Wind(0,0),Wind(0,0)])
        cellFinish = Cell(0,1,[Wind(0,0),Wind(0,0),Wind(0,0)])
        cellTarget1 = TargetCell(0,2,[Wind(0,0),Wind(0,0),Wind(0,0)])
        cellTarget2 = TargetCell(0,3,[Wind(0,0),Wind(0,0),Wind(0,0)])
        cellStart.addNeighbor(cellStart)
        cellStart.addNeighbor(cellFinish)
        cellStart.addTarget(cellTarget1)
        cellFinish.addTarget(cellTarget2)
        balloon = Balloon(cellStart)
        assert len(cellTarget1.coverBy)==0 and len(cellTarget2.coverBy)==0
        balloon.applyWind()
        assert len(cellTarget1.coverBy)==1 and len(cellTarget2.coverBy)==0
        assert balloon.cell is cellStart
        balloon.moveAlt(1)
        balloon.applyWind()
        assert len(cellTarget1.coverBy)==0 and len(cellTarget2.coverBy)==1
        assert balloon.cell is cellFinish