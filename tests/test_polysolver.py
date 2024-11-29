import pytest
from polysolver import stringifySolution
from simulation import ResultData

class TestPolysolver:

    def test_stringifySolution(self):
        nbT = 4
        res = ResultData(0, [
            [1, 0, 1, -1],
            [0, 0, 1, -1],
            [1, 0],
            [1, 0, 1, -1],
            ])
        sol = """1 0 1 1\n0 0 0 0\n1 1 0 1\n-1 -1 0 -1"""
        assert stringifySolution(res, nbT) == sol

        nbT = 5
        sol = """1 0 1 1\n0 0 0 0\n1 1 0 1\n-1 -1 0 -1\n0 0 0 0"""
        assert stringifySolution(res, nbT) == sol
    

    def test_solve(self):       #TODO: make this
        ...