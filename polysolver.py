"""Module de résolution du projet Poly#.
"""

from brain import *
from polyparser import ParserData
from simulation import ResultData, Simulation
from cellMap import CellMap

def solve(challenge: ParserData) -> str: #TODO: add test
    """Solve a given challenge while checking the consistency of the result
    """
    cellMap = CellMap(challenge)
    brain = RandomBrain()
    brain = ClosestBrain(challenge.turns)
    brain = VerifyBrain("b_small.txt")
    brain = TreeBrain(cellMap, wideness=500, deepness=50, debugInfo=True)
    simulation = Simulation(challenge, brain, cellMap)
    for n, _ in enumerate(simulation.runIter()):
        #Add here some visualitation or some test
        pass
    result = simulation.result()
    print(f"The simulation reached {result.nbPoints} points.")
    return stringifySolution(result, simulation.ROUNDS)


def stringifySolution(result:ResultData, nbTurn:int) -> str:
    """Transform results in a conform textual ouput"""
    solution = ""
    for turn in range(nbTurn):
        for balloon in range(len(result.tracking)):
            if len(result.tracking[balloon]) > turn:
                solution += str(result.tracking[balloon][turn]) + " "
            else:
                solution += "0 "
        solution = solution[:-1] + "\n"
    return solution[:-1]

def getScoreSolution(file: str, challenge: ParserData) -> int:
    """Résout un challenge donné.
    """
    cellMap = CellMap(challenge)
    brain = VerifyBrain(file)
    simulation = Simulation(challenge, brain, cellMap)
    for _ in simulation.runIter():
        #Add here some visualitation or some test
        pass
    result = simulation.result()
    return result.nbPoints

def saveSolution(fileName: str, file: str) -> None:
    assert fileName.endswith('.txt')==True, "the file name has not the right extension, try again :)"
    with open(fileName, "w") as f:
        f.write(file)
    print(f"The file {fileName} has been saved")