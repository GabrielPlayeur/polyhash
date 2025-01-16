import pytest
import os

from polyparser import parseChallenge
from simulation import Simulation
from brain.verifyBrain import VerifyBrain

#TODO: fix with new rules
class TestHistory:
        
        NUM_TEST = 100
        NAME_FILE = "tests/data/sol_test_history.txt"

        
        def verifyIfFileExist(self):
                if not os.path.exists("tests/data"):
                        os.mkdir('tests/data')
                if not os.path.exists(self.NAME_FILE):
                        data = "0\n1\n1\n-1\n0"
                        with open(self.NAME_FILE, "w") as f:
                                f.write(data)

        

        def test_history_PrevTurn_OneTurn(self): 
                '''Mise en place de la simulation'''
                self.verifyIfFileExist()
                challengeTest = parseChallenge(f"./challenges/a_example.in")
                testBrain = VerifyBrain("tests/data/sol_test_history.txt")
                simulation = Simulation(challengeTest, testBrain)    
                
                '''Jeu de donnée'''

                balloonsFirstTurn = [(1,2),0]
                nbPointsFirstTurn = 0
                
                '''Execution des fonctions'''

                simulation.nextTurn()
                simulation.prevTurn()

                assert simulation.resultData.nbPoints == nbPointsFirstTurn

                for balloon in simulation.balloons:
                        assert balloon.cell.pos == balloonsFirstTurn[0]
                        assert balloon.alt == balloonsFirstTurn[1]


        def test_history_PrevTurn_Multiple(self):
                '''Mise en place de la simulation'''
                self.verifyIfFileExist()
                challengeTest = parseChallenge(f"./challenges/a_example.in")
                testBrain = VerifyBrain("tests/data/sol_test_history.txt")
                simulation = Simulation(challengeTest, testBrain)    
                
                '''Jeu de donnée'''

                balloonDataAtTurn = [((1,2),0),((1,2),0),((1,3),1),((0,3),2),((0,4),1),((0,0),1)]
                nbPointsAtTurn = [0,1,1,3,4,5]

                '''Execution des fonctions '''

                for i in range(len(nbPointsAtTurn)-1):
                        simulation.nextTurn()
                for i in range(len(nbPointsAtTurn)-2,-1,-1):
                        simulation.prevTurn()
                        assert simulation.resultData.nbPoints == nbPointsAtTurn[i]

                        for balloon in simulation.balloons:
                                assert balloon.cell.pos == balloonDataAtTurn[i][0]
                                assert balloon.alt == balloonDataAtTurn[i][1]

                


