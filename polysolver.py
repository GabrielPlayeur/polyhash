#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""



from polyparser import ParserData
from simulation import ResultData, Simulation


def solve(challenge: ParserData):
    """Résout un challenge donné.
    """
    
    simulation = Simulation(challenge)
    result = simulation.run()
    
    print(f"La simulation a atteint {result.nbPoints} points. !!!!! trop fort les gars")
    return stringifySolution(result, simulation.ROUNDS)


def stringifySolution(result:ResultData, nbTurn:int) -> str:
    #TODO: write it !

    solution = ""
    
    for balloonPath in result.tracking:
        i = 0
        for move in balloonPath:
            i += 1
            solution += str(move) + " "

        while i < nbTurn:
            solution += "0 "
            i += 1

        solution = solution[:-1] + "\n"

    return solution



def getScoreSolution(file):
    ...


def saveSolution(fileName, file):
    assert fileName[-4:] == ".sol", "the file name has not the right extension, try again :)"
    with open(fileName, "w") as f:
        f.write(file)
    print(f"The file {fileName} has been saved")