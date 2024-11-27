"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""
import re
import os
from dataclasses import dataclass

@dataclass
class ParserData:
    rows: int
    columns: int
    altitudes: int
    targets_number: int
    radius: int
    balloons: int
    turns: int
    starting_cell: tuple[int,int]
    targets_pos: set[tuple[int,int]]
    winds: list[list[list[tuple[int,int]]]]

def parseChallenge(filename: str) -> ParserData:
    """
    Reads a challenge file and extracts the necessary information.
    args:
        filename: path to a challenge file
    return:
        data: challengeextracts information
    """
    assert os.path.exists(filename) == True, f"The given file's path didn't exist in ./challenges/: {filename}"
    data = {}
    with open(filename, 'r') as f:
        line = re.sub(r'\s*#.*', '', f.readline().strip())
        data['rows'], data['columns'], data['altitudes'] = [ int(v) for v in line.split() ]
        line = re.sub(r'\s*#.*', '', f.readline().strip())
        data['targets_number'], data['radius'], data['balloons'], data['turns'] = [ int(v) for v in line.split() ]
        line = re.sub(r'\s*#.*', '', f.readline().strip())
        row,col = [ int(v) for v in line.split() ]
        data['starting_cell'] = (row,col)
        data['targets_pos'] = set()
        for _ in range(data['targets_number']):
            line = re.sub(r'\s*#.*', '', f.readline().strip())
            row,col = [int(v) for v in line.split()]
            data['targets_pos'].add((row,col))
        data['winds'] = [ [ [] for _ in range(data['columns'])] for _ in range(data['rows'])]
        for _ in range(data['altitudes']):
            for i in range(data['rows']):
                line = re.sub(r'\s*#.*', '', f.readline().strip())
                colWinds = [int(v) for v in line.split()]
                for j in range(0,len(colWinds),2):
                    row,col = colWinds[j],colWinds[j+1]
                    data['winds'][i][j//2].append((row,col))
    return ParserData(data['rows'],
                      data['columns'],
                      data['altitudes'],
                      data['targets_number'],
                      data['radius'],
                      data['balloons'],
                      data['turns'],
                      data['starting_cell'],
                      data['targets_pos'],
                      data['winds']
                      )