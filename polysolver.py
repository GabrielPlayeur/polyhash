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
    simulation.run()
    

    a_solution = str()

    return a_solution


def stringifyingSolution(solution:ResultData) -> str:
    #TODO: write it !

    result = ""

    return result



def getScoreSolution(file):
    ...


def saveSolution(fileName, file):
    ...
