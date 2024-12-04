import pytest

from polyparser import parseChallenge
from simulation import Simulation

class TestHistory:
        def testOnePrevTurn(self):
                challengeTest = parseChallenge(f"./challenges/a_example.in")
                simulation = Simulation(challengeTest)
                
                balloonsFirstTurn = []
                assert simulation.balloons
                for balloon in simulation.balloons:
                        balloonsFirstTurn.append(balloon)

                assert simulation.resultData.nbPoints != None
                nbPointsFirstTurn = simulation.resultData.nbPoints
                assert type(nbPointsFirstTurn) == int
                
                '''Execution of the functions'''

                simulation.nextTurn()
                simulation.prevTurn()

                assert simulation.resultData.nbPoints == nbPointsFirstTurn

                i = 0
                for balloon in simulation.balloons:
                        assert balloon.cell == balloonsFirstTurn[i].cell
                        assert balloon.alt == balloonsFirstTurn[i].alt
                        i += 1

