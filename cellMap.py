"""Module.
"""

from __future__ import annotations
from objects import Wind, Cell, TargetCell
from polyparser import ParserData, parseChallenge
import pickle

#TODO: change doc in english
class CellMap:
    """
    Cette classe représente la carte des vents sous forme d'une matrice de cellules.
    """

    def __init__(self, parserData: ParserData) -> None:
        assert parserData is not None, "<parserData> is None"
        self.rows: int = parserData.rows
        self.columns: int = parserData.columns
        self.altitudes: int = parserData.altitudes
        self.turns: int = parserData.turns
        self.ballons: int = parserData.balloons
        self.radius: int = parserData.radius
        self.startingCell: Cell
        self.outsideCell: Cell = Cell(-1,-1,[])

        self.map:list[list[Cell]] = []

        self._initialize(parserData)
        self._defineTargetRange(parserData)
        self._createGraph()

    def _initialize(self, parserData: ParserData) -> None:
        """Initialisation de la matrice de cellule"""
        self.map = []

        for row in range(self.rows):
            self.map.append([])
            for col in range(self.columns):
                winds: list[Wind] = []
                for vec in parserData.winds[row][col]:
                    winds.append(Wind(vec[0], vec[1]))

                if (row, col) in parserData.targets_pos:
                    cell = TargetCell(row, col, winds)
                else:
                    cell = Cell(row, col, winds)

                if (cell.row, cell.col) == parserData.starting_cell:
                    self.startingCell = cell

                self.map[row].append(cell)

        assert self.startingCell is not None

    def _defineTargetRange(self, parserData: ParserData) -> None:
        """Defini les cellules couvertes par une target"""
        for targetPos in parserData.targets_pos:
            target = self.map[targetPos[0]][targetPos[1]]

            #pour limiter le rayon de recherche, on teste toutes les cellules dans le carré de coté radius centré sur target
            northSquare = max(target.row-self.radius, 0)
            southSquare = min(target.row+self.radius+1, self.rows)
            eastSquare = target.col-self.radius
            westSquare = target.col+self.radius+1

            for row in range(northSquare, southSquare):
                for col in range(eastSquare, westSquare):
                    cell = self.map[row][col%self.columns]
                    if self.inRange(target, cell):
                        cell.addTarget(target)

    def _createGraph(self) -> None:
        """Crée un graph à partir de la martice de cellule et de celle des vents"""
        assert self.startingCell is not None, "Impossible de créer le graph: startingCell is None"
        for row in range(self.rows):
            for col in range(self.columns):
                cell = self.map[row][col]
                for wind in cell.getWinds():
                    dRow, dCol = wind.vec
                    if 0 <= row+dRow < self.rows:
                        neighbors = self.map[row+dRow][(col+dCol)%self.columns]
                        cell.addNeighbor(neighbors)
                    else:
                        cell.addNeighbor(self.outsideCell)

                assert len(cell.neighbors) == self.altitudes+1, f"La cellule {cell} n'a pas {self.altitudes} cellules adjacentes"

    def getCell(self, row: int, col: int) -> Cell:
        assert 0 <= row < self.rows, "row out of range"
        assert 0 <= col < self.columns, "row out of range"
        return self.map[row][col]

    def inRange(self, target: Cell, cell: Cell) -> bool:
        """Retourne vrai si la cellule est dans le rayon <self.radius> de target"""
        columndist = lambda c1, c2: min(abs(c1-c2), self.columns - abs(c1-c2))
        return (cell.row - target.row)**2 + columndist(cell.col, target.col)**2 <= self.radius**2

    def save(self, fileName: str) -> None:
        """
        Sauvegarde l'objet CellMap dans un fichier binaire.

        :param fileName: Nom du fichier. L'extension doit être '<fileName>.poly#'
        """
        assert fileName[-6:] == ".poly#", f"{fileName} n'a pas l'extension '.poly#'"

        try:
            with open(fileName, 'wb') as file:
                pickle.dump(self, file)
            print(f"Sauvegarde effectuée avec succès dans '{fileName}'.")
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la sauvegarde") from e

    @staticmethod
    def load(fileName: str) -> CellMap:
        """
        Charge un objet CellMap depuis un fichier binaire.

        :param fileName: Nom du fichier. L'extension doit être '<fileName>.poly#'
        :return: Une instance de CellMap.
        :raises Exception: Si une erreur se produit lors du chargement.
        """
        assert fileName[-6:] == ".poly#", f"{fileName} n'a pas l'extension '.poly#'"
        try:
            with open(fileName, 'rb') as file:  # 'rb' pour lecture en binaire
                cell_map = pickle.load(file)
            print(f"Carte chargée avec succès depuis '{fileName}'.")
            return cell_map
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement de la carte depuis '{fileName}'") from e

    def __str__(self) -> str:
        """Affiche la carte des vents à l'altitude donnée"""
        centerize = lambda content: f"{content:^3}"
        text = f"Affichage de la carte de taille {self.rows}x{self.columns}\n\n" + centerize("")
        for i in range(self.columns):
            text += centerize(i)

        for row in range(self.rows):
            text += "\n" + centerize(row)

            for col in range(self.columns):
                cell:Cell = self.map[row][col]
                if cell is self.startingCell:
                    text += centerize("S" if type(cell) == TargetCell else "s")
                elif type(cell) == TargetCell:
                    text += centerize("T")
                elif len(cell.targets) > 0:
                    text += centerize("P")
                else:
                    text += centerize("_")
        return text + "\n"