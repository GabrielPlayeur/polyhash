"""Module.
"""

from __future__ import annotations
from objects import Wind, Cell, TargetCell
from polyparser import ParserData
import pickle

class CellMap:
    """
    This class represents the wind map as a matrix of cells.
    """

    def __init__(self, parserData: ParserData) -> None:
        assert parserData is not None, "<parserData> is None"
        self.rows: int = parserData.rows
        self.columns: int = parserData.columns
        self.altitudes: int = parserData.altitudes
        self.turns: int = parserData.turns
        self.balloons: int = parserData.balloons
        self.radius: int = parserData.radius
        self.startingCell: Cell
        self.outsideCell: Cell = Cell(-1,-1,[])

        self.map:list[list[Cell]] = []

        self._initialize(parserData)
        self._defineTargetRange(parserData)
        self._createGraph()

    def _initialize(self, parserData: ParserData) -> None:
        """Initialization of the cell matrix"""
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
        """Defines the cells covered by a target"""
        ratio = 0
        for targetPos in parserData.targets_pos:
            target = self.map[targetPos[0]][targetPos[1]]

            #to limit the search radius, we test all the cells in the radius square centered on target
            northSquare = max(target.row-self.radius, 0)
            southSquare = min(target.row+self.radius+1, self.rows)
            eastSquare = target.col-self.radius
            westSquare = target.col+self.radius+1

            for row in range(northSquare, southSquare):
                for col in range(eastSquare, westSquare):
                    cell = self.map[row][col%self.columns]
                    if self.inRange(target, cell):
                        cell.addTarget(target)
                        ratio += 1

    def _createGraph(self) -> None:
        """Creates a graph from the cell and wind martices"""
        assert self.startingCell is not None, "Impossible to create the graph: startingCell is None"
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

                assert len(cell.neighbors) == self.altitudes+1, f"The cell {cell} hasn't {self.altitudes} adjacents cells"

    def getCell(self, row: int, col: int) -> Cell:
        assert 0 <= row < self.rows, "row out of range"
        assert 0 <= col < self.columns, "row out of range"
        return self.map[row][col]

    def inRange(self, target: Cell, cell: Cell) -> bool:
        """Returns true if the cell is within the radius <self.radius> of target"""
        columndist = lambda c1, c2: min(abs(c1-c2), self.columns - abs(c1-c2))
        return (cell.row - target.row)**2 + columndist(cell.col, target.col)**2 <= self.radius**2

    def save(self, fileName: str) -> None:
        """
        Saves the CellMap object in a binary file.

        :param fileName: File name. The extension must be '<fileName>.poly#'.
        """
        assert fileName[-6:] == ".poly#", f"{fileName} hasn't the extension '.poly#'"

        try:
            with open(fileName, 'wb') as file:
                pickle.dump(self, file)
            print(f"Successful save in '{fileName}'.")
        except Exception as e:
            raise RuntimeError(f"Saving error") from e

    @staticmethod
    def load(fileName: str) -> CellMap:
        """
        Loads a CellMap object from a binary file.

        :param fileName: File name. The extension must be '<fileName>.poly#'.
        :return: An instance of CellMap.
        :raises Exception: If an error occurs during loading.
        """
        assert fileName[-6:] == ".poly#", f"{fileName} n'a pas l'extension '.poly#'"
        try:
            with open(fileName, 'rb') as file:  # 'rb' pour lecture en binaire
                cell_map = pickle.load(file)
            print(f"Card successfully loaded from '{fileName}'.")
            return cell_map
        except Exception as e:
            raise RuntimeError(f"Error while loading the map from '{fileName}'") from e

    def __str__(self) -> str:
        """Displays wind map at given altitude"""
        centerize = lambda content: f"{content:^3}"
        text = f"Display of the map : {self.rows}x{self.columns}\n\n" + centerize("")
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