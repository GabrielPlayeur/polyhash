#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""

from observer import Observer
from polyparser import ParserData
from simulation import ResultData, Simulation


def solve(challenge: ParserData):
    """Solve a given challenge while checking the consistency of the result
    """
    
    simulation = Simulation(challenge)
    observer = Observer(challenge)

    for turn, partialResult in simulation.run():
        observer.inspect(turn, partialResult)
    
    result = simulation.result()
    
    print(f"La simulation a atteint {result.nbPoints} points.")
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



def getScoreSolution(file):
    ...


def saveSolution(fileName, file):
    assert fileName[-4:] == ".txt", "the file name has not the right extension, try again :)"
    with open(fileName, "w") as f:
        f.write(file)
    print(f"The file {fileName} has been saved")