import pytest
from objects import Cell, Wind, Balloon

class TestBalloon:

    def test_balloon_init(self):
        cell = Cell(0,0,tuple([Wind(0,0),Wind(0,0)]))
        balloon = Balloon(cell)
        assert type(balloon) == Balloon
        assert balloon.alt==0
        assert balloon.altMax==2

    def test_balloon_moveAlt(self):
        cell = Cell(0,0,tuple([Wind(0,0),Wind(0,0)]))
        balloon = Balloon(cell)
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