import pytest
import os
from polysolver import stringifySolution, getScoreSolution, saveSolution
from polyparser import parseChallenge
from simulation import ResultData
from brain import VerifyBrain

class TestPolysolver:
    NAME_FILE = "tests/data/test_data_verifyBrain.txt"
    def verifyIfFileExist(self):
        if not os.path.exists("tests/data"):
            os.mkdir('tests/data')
        if not os.path.exists(self.NAME_FILE):
            data = "0\n1\n1\n-1\n0"
            with open(self.NAME_FILE, "w") as f:
                f.write(data)

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

    def test_getScoreSolution(self):
        self.verifyIfFileExist()
        challenge = parseChallenge(f"./challenges/a_example.in")
        scr = getScoreSolution(self.NAME_FILE, challenge)
        assert scr == 5

    def test_saveSolution(self):
        data = "data val test temp. Have to be delete."
        fileName = "tempDataTest.txt"
        if os.path.exists(fileName):
            os.remove(fileName)
        assert os.path.exists(fileName)==False, f"Error the file already exist pls delete it before running the test. {fileName}"
        saveSolution(fileName, data)
        assert os.path.exists(fileName)==True
        os.remove(fileName)
        assert os.path.exists(fileName)==False, f"Error the file didn't have been delete during the test process please delete it. {fileName}"
        with pytest.raises(AssertionError):
            saveSolution("test", data)