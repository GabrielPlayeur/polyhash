import pytest
from objects import Balloon, Cell, Wind
from brain import RandomBrain



class TestRandomBrain:
    NUM_TEST = 10
    def test_randomBrain_solve(self):
        brain = RandomBrain()
        cell = Cell(0,0, (Wind(0,0), Wind(0,0),Wind(0,0)))
        balloon = Balloon(cell)
        res = set([0,1])
        for _ in range(self.NUM_TEST):
            assert brain.solve(balloon) in res
        balloon.moveAlt(1)
        balloon.moveAlt(1)
        res = set([0,1,-1])
        for _ in range(self.NUM_TEST):
            assert brain.solve(balloon) in res
        balloon.moveAlt(1)
        res = set([0,-1])
        for _ in range(self.NUM_TEST):
            assert brain.solve(balloon) in res