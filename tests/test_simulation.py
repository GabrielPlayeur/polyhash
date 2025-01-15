import os
from simulation import Simulation
from polyparser import parseChallenge
from brain import VerifyBrain
from cellMap import CellMap

#TODO: fix with new rules
class TestSimulation:
    NAME_FILE = "tests/data/test_data_verifyBrain.txt"
    def verifyIfFileExist(self):
        if not os.path.exists("tests/data"):
            os.mkdir('tests/data')
        if not os.path.exists(self.NAME_FILE):
            data = "0\n1\n1\n-1\n0"
            with open(self.NAME_FILE, "w") as f:
                f.write(data)

    def test_simulation_init(self):
        self.verifyIfFileExist()
        challenge = parseChallenge('challenges/a_example.in')
        cellMap = CellMap(challenge)
        brain = VerifyBrain(self.NAME_FILE)
        sim = Simulation(challenge, brain, cellMap)
        assert type(sim) is Simulation

    def test_simulation_runIter(self):
        self.verifyIfFileExist()
        challenge = parseChallenge('challenges/a_example.in')
        cellMap = CellMap(challenge)
        brain = VerifyBrain(self.NAME_FILE)
        sim = Simulation(challenge, brain, cellMap)
        scr = [-1,1,1,3,4,5]
        mvt = [0,1,1,-1,0]
        i = 1
        for rnd, res in sim.runIter():
            assert rnd==i
            assert res.nbPoints==scr[i]
            assert res.tracking[0][i-1]==mvt[i-1]
            i+=1

    def test_simulation_nextTurn(self):
        self.verifyIfFileExist()
        challenge = parseChallenge('challenges/a_example.in')
        cellMap = CellMap(challenge)
        brain = VerifyBrain(self.NAME_FILE)
        sim = Simulation(challenge, brain, cellMap)
        scr = [1,1,3,4,5]
        mvt = [0,1,1,-1,0]
        alt = [0,1,2,1,1]
        pos = [(1,2),(1,3),(0,3),(0,4),(0,0)]
        for i in range(5):
            sim.nextTurn()
            assert sim.balloons[0].alt==alt[i]
            assert sim.balloons[0].cell.pos==pos[i]
            assert sim.resultData.tracking[0][i]==mvt[i]
            assert sim.resultData.nbPoints==scr[i]
            assert sim.current_round==i+1

    def test_simulation_result(self):
        self.verifyIfFileExist()
        challenge = parseChallenge('challenges/a_example.in')
        cellMap = CellMap(challenge)
        brain = VerifyBrain(self.NAME_FILE)
        sim = Simulation(challenge, brain, cellMap)
        mvt = [0,1,1,-1,0]
        assert sim.result().nbPoints==0
        assert len(sim.result().tracking)==1
        assert sim.result().tracking[0]==[]
        sim.run()
        assert sim.result().nbPoints==5
        assert len(sim.result().tracking)==1
        assert sim.result().tracking[0]==mvt