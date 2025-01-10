import pytest

from observer import XYZ, Observer
from polyparser import parseChallenge
from simulation import ResultData


@pytest.fixture
def observer_setupA():
    parser = parseChallenge("./challenges/a_example.in")
    obs = Observer(parser)
    return obs, parser

@pytest.fixture
def observer_setupB():
    parser = parseChallenge("./challenges/b_small.in")
    obs = Observer(parser)
    return obs, parser

class TestObserver():
    def test_checkAlt(self, observer_setupA):
        obs, parser = observer_setupA
        assert obs._checkAlt(0, 1) == 1, "decollage"
        assert obs._checkAlt(0, 0) == 0, "sol"
        assert obs._checkAlt(0, -1) == 0, "enterrement"
        assert obs._checkAlt(1, -1) == 0, "ratterissage"
        assert obs._checkAlt(2, -1) == -1, "descente"
        assert obs._checkAlt(2, 0) == 0, "h max"
        assert obs._checkAlt(parser.altitudes, 1) == 0, "depassement"

    def test_inRange(self, observer_setupA):
        obs, _ = observer_setupA
        assert obs._inRange(XYZ(0, 2, 0), XYZ(0, 2, 0)), "the cell is not in range of itself"

    def test_targetInRange(self, observer_setupA):
        obs, _ = observer_setupA
        a_small = [
            [1, 1, 1, 2, 1],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            ]
        senarios = [XYZ(0, 0, 0), XYZ(1, 0, 0), XYZ(1, 2, 0), XYZ(0, 2, 0)]
        for s in senarios:
            targets = obs._targetInRange(s)
            for tar in targets:
                assert a_small[tar.row][tar.col] > 0, f"Failed for scenario {s}"

        assert len(obs._targetInRange(XYZ(0, 3, 0))) == 2, ""

    def test_observer(self, observer_setupA):
        obs, _ = observer_setupA
        assert obs.inspect(1, ResultData(0, [[1]])), "pos: (1, 3)"
        assert obs.inspect(2, ResultData(2, [[1, 1]])), "pos: (0, 3)"
        assert obs.inspect(3, ResultData(3, [[1, 1, -1]])), "pos: (0, 4)"
        assert obs.inspect(4, ResultData(4, [[1, 1, -1, 0]])), "pos: (0, 0)"