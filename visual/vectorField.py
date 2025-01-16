import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import matplotlib.pyplot as plt

from cellMap import CellMap
from polyparser import parseChallenge

def create(challenge: str) -> None:
    cellMap = CellMap(parseChallenge(f"./challenges/{challenge}.in"))
    for alt_idx in range(1, cellMap.altitudes + 1):
        X, Y, U, V = [], [], [], []
        for i in range(cellMap.rows):
            for j in range(cellMap.columns):
                X.append(j)
                Y.append(i)
                U.append(cellMap.map[i][j].getWindsByAlt(alt_idx).dCol)
                V.append(cellMap.map[i][j].getWindsByAlt(alt_idx).dRow)
        
        # Création de la figure
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, color='blue')
        
        # Ajouter un quadrillage
        ax.set_xticks(np.arange(-0.5, cellMap.columns, 1))
        ax.set_yticks(np.arange(-0.5, cellMap.rows, 1))
        ax.grid(color='black', linestyle='-', linewidth=0.5)
        
        # Paramètres de la grille
        ax.set_xlim(-0.5, cellMap.columns - 0.5)
        ax.set_ylim(-0.5, cellMap.rows - 0.5)
        ax.set_aspect('equal')        
        ax.invert_yaxis()
        
        # Titre et labels
        ax.set_title(f'Champs de vecteurs à altitude {alt_idx}')
        ax.set_xlabel('Colonnes')
        ax.set_ylabel('Lignes')

        # Afficher la figure
        plt.show()

if __name__ == '__main__':
    name = "a_example"
    name = "c_medium"
    name = "d_final"
    name = "b_small"

    create(name)
