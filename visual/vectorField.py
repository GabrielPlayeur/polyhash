import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import matplotlib.pyplot as plt

from cellMap import CellMap
from polyparser import parseChallenge

def create(challenge: str) -> None:
    cellMap = CellMap(parseChallenge(f"./challenges/{name}.in"))
    for alt_idx in range(1,cellMap.altitudes+1):
        X, Y, U, V = [], [], [], []
        for i in range(cellMap.rows):
            for j in range(cellMap.columns):
                X.append(j)
                Y.append(i)
                U.append(cellMap.map[i][j].getWindsByAlt(alt_idx).dCol)
                V.append(cellMap.map[i][j].getWindsByAlt(alt_idx).dRow)
        plt.figure(figsize=(6, 6))
        plt.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, color='blue')
        plt.title(f'Champs de vecteurs à altitude {alt_idx}')
        plt.xlim(-0.5, cellMap.columns - 0.5)
        plt.ylim(-0.5, cellMap.rows - 0.5)
        plt.gca().set_aspect('equal')
        plt.xlabel('Colonnes')
        plt.ylabel('Lignes')
        plt.show()

if __name__ == '__main__':
    name = "a_example"
    name = "c_medium"
    name = "d_final"
    name = "b_small"

    create(name)
