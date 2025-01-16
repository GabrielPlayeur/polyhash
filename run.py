import os

from brain import *
from polysolver import stringifySolution, saveSolution
from polyparser import ParserData
from simulation import ResultData, Simulation
from cellMap import CellMap
from polyparser import parseChallenge

CHALLENGE_NAME = "d_final"
WID = 500
DEEP = 100

challenge = parseChallenge(f"./challenges/{CHALLENGE_NAME}.in")
while True:
    cellMap = CellMap(challenge)
    brain = TreeBrain(cellMap, wideness=WID, deepness=DEEP, debugInfo=True)
    simulation = Simulation(challenge, brain, cellMap)
    for n, _ in enumerate(simulation.runIter()):
        pass
    result = simulation.result()
    print(f"The simulation reached {result.nbPoints} points.")
    solution = stringifySolution(result, simulation.ROUNDS)
    FILE_NAME = f"output/out_{CHALLENGE_NAME}_{WID}_{DEEP}_{result.nbPoints}.txt"
    if not os.path.exists(FILE_NAME):
        saveSolution(FILE_NAME,solution)