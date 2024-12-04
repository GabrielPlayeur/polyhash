import pytest
import os
from brain import VerifyBrain

class TestVerifyBrain:
    NAME_FILE = "tests/data/test_data_verifyBrain.txt"
    def verifyIfFileExist(self):
        if not os.path.exists("tests/data"):
            os.mkdir('tests/data')
        if not os.path.exists(self.NAME_FILE):
            data = "0\n1\n1\n-1\n0"
            with open(self.NAME_FILE, "w") as f:
                f.write(data)

    def test_verifyBrain_load(self):
        self.verifyIfFileExist()
        brain = VerifyBrain(self.NAME_FILE)
        assert len(brain.lines) > 0 and len(brain.lines[0]) > 0
        with pytest.raises(AssertionError):
           VerifyBrain("azertyuiuytrezertyuiuytrertyuiuytrertyuiuytreztyuioezryuiopudtyuioptyuioputyuiopezqretyuiopse")

    def test_verifyBrain_solve(self):
        self.verifyIfFileExist()
        brain = VerifyBrain(self.NAME_FILE)
        path = [0,1,1,-1,0]
        for i in range(5):
            assert path[i] == brain.solve(0,i)
        with pytest.raises(AssertionError):
            brain.solve(-1, 0)
        with pytest.raises(AssertionError):
            brain.solve(15, 0)
        with pytest.raises(AssertionError):
            brain.solve(0, -1)
        with pytest.raises(AssertionError):
            brain.solve(0, 15)