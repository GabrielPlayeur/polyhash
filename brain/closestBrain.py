from .brainInit import *
from collections import defaultdict, deque
from functools import cache

class ClosestBrain(Brain):
    """A concrete implementation of the Brain class using a pathfinding approach.

    This class utilizes Dijkstra's algorithm to determine the shortest path for a balloon.
    It maintains a graph representation of possible moves and tracks covered cells.
    """

    def __init__(self, maxTurn: int) -> None:
        self.maxTurn = maxTurn
        self.covered: dict[tuple[int, int], int] = dict()
        self.graph: dict[tuple[int, int, int], set] = defaultdict(set)
        self.balloonMove: dict[Balloon, dict] = {}
        self.addOutsideCell()

    def solve(self, balloon: Balloon, map: list[list[Cell]]) -> int:
        """Determine the next move for a balloon using pathfinding.

        Returns:
            int: The next movement direction for the balloon.
        """
        savePath = self.balloonMove.get(balloon)
        if savePath is not None and savePath['idx'] < len(savePath['moves']):
            move = savePath['moves'][savePath['idx']]
            savePath['idx'] += 1
            return move
        if savePath is not None:
            self.removeCoveredCell(balloon.cell)
        cell, moves = self.dijkstra(balloon.cell, balloon.alt)
        self.addCoveredCell(map[cell[0]][cell[1]])
        self.balloonMove[balloon] = {'idx': 1, 'moves': moves}
        savePath = self.balloonMove[balloon]
        return moves[0]

    def dijkstra(self, start: Cell, alt: int) -> tuple[tuple[int, int], list[int]]:
        """Perform Dijkstra's algorithm to find the optimal path.

        Args:
            start (Cell): The starting cell for the pathfinding.
            alt (int): The starting altitude.

        Returns:
            tuple: The best cell position and the list of movements to reach it.
        """
        self.givePoint.cache_clear()
        dist = defaultdict(lambda: (float('inf'), []))
        minKey, minTurn = (-1, -1), float('inf')
        visited: set[tuple[int, int, int]] = set()
        nextCells = deque([(start, alt, 0, [])])
        while len(nextCells):
            for _ in range(len(nextCells)):
                cur, curAlt, tu, path = nextCells.popleft()
                key = (cur.row, cur.col, curAlt)
                if key in visited or tu > self.maxTurn:
                    continue
                if self.givePoint(cur) and dist[cur.pos][0] > tu:
                    dist[cur.pos] = (tu, path)
                    if tu < minTurn:
                        minKey = cur.pos
                        minTurn = tu
                self.addEdge(cur, curAlt)
                for nCell, dAlt in self.graph[key]:
                    nAlt = curAlt + dAlt
                    nKey = (nCell.row, nCell.col, nAlt)
                    if nKey not in visited:
                        nextCells.append((nCell, nAlt, tu + 1, path + [dAlt]))
                visited.add(key)
        moves: list[int] = dist[minKey][1]
        return minKey, moves if len(moves) > 0 else [0]

    def addEdge(self, cell: Cell, alt: int) -> None:
        """Add edges to the graph for movement possibilities.
        """
        key = (cell.row, cell.col, alt)
        if self.graph.get(key) is not None:
            return
        self.graph[key].add((cell.getNeighbor(alt), 0))
        if alt - 1 > 0:
            self.graph[key].add((cell.getNeighbor(alt - 1), -1))
        if alt + 1 < len(cell.neighbors):
            self.graph[key].add((cell.getNeighbor(alt + 1), 1))

    @cache
    def givePoint(self, cell: Cell) -> bool:
        """Determine if a cell is a valid target.
        """
        for t in cell.targets:
            if t.pos not in self.covered.keys() or self.covered[t.pos] == 0:
                return True
        return False

    def addOutsideCell(self) -> None:
        """Initialize graph entries for outside cells."""
        for alt in range(self.maxTurn):
            self.graph[(-1, -1, alt)] = set()

    def addCoveredCell(self, cell: Cell) -> None:
        """Mark a cell as covered.
        """
        for t in cell.targets:
            if self.covered.get(t.pos) is None:
                self.covered[t.pos] = 0
            self.covered[t.pos] += 1

    def removeCoveredCell(self, cell: Cell) -> None:
        """Unmark a cell as covered.
        """
        for t in cell.targets:
            if self.covered.get(t.pos) is None:
                self.covered[t.pos] = 1
            self.covered[t.pos] -= 1