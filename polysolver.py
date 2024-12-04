"""Module de résolution du projet Poly#.
"""

from brain import RandomBrain, VerifyBrain
from polyparser import ParserData
from simulation import ResultData, Simulation

def solve(challenge: ParserData) -> str: #TODO: add test
    """Résout un challenge donné.
    """
    brain = RandomBrain()
    simulation = Simulation(challenge, brain)
    for _ in simulation.runIter():
        #Add here some visualitation or some test
        pass
    result = simulation.result()
    print(f"La simulation a atteint {result.nbPoints} points. !!!!! trop fort les gars")
    return stringifySolution(result, simulation.ROUNDS)

def stringifySolution(result: ResultData, nbTurn: int) -> str:
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
    brain = VerifyBrain(file)
    simulation = Simulation(challenge, brain)
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