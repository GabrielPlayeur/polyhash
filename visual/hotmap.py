import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import matplotlib.pyplot as plt

from cellMap import CellMap
from polyparser import parseChallenge

def create(challenge: str) -> None:
    cellMap = CellMap(parseChallenge(f"./challenges/{name}.in"))
    heatmap_data = [[len(cell.targets) for cell in row] for row in cellMap.map]
    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Nombre d\'éléments dans targets')
    plt.title('Heatmap basée sur le nombre d\'éléments dans targets')
    plt.xlabel('Colonnes')
    plt.ylabel('Lignes')
    plt.show()

if __name__ == '__main__':
    name = "a_example"
    name = "b_small"
    name = "c_medium"
    name = "d_final"
    create(name)
