from .brainInit import Brain
from collections import deque
from .node import Node
from cellMap import CellMap
from objects import TargetCell, Cell
from time import time
from random import randint

class TreeBrain(Brain):
    def __init__(self, graph: CellMap, deepness: int, debugInfo=False) -> None:
        """
        Initialize a Tree instance.
            -> There two majors ways of using this class:
            - by creating unique Tree and refreshing itself every iteration (very bugged but optimized)
            - by creating a new Tree every iteration and passing it the new coveredTarget argument with a context manager to limit the memory impact (not opti but sure)

        Args:
            `graph` (CellMap):
                The graph representation of the environment, which serves as the base for constructing the tree.

            `deepness` (int): 
                The maximum depth to which the tree will be expanded, i.e the coefficeint of the linear increasement
                of the number of nodes explored each stage of the tree.

            `coveredTarget` (dict[int, set[TargetCell]], optional):
                A dictionary mapping balloon indices to sets of target cells that have already been covered.
                Defaults to an empty dictionary.

            `debugInfo` (bool, optional):
                Flag to enable or disable debug information. If True, additional debug output will be provided during execution. Defaults to False.
        """
        self.graph: CellMap = graph
        self.coveredTarget: list[set[TargetCell]] = [set() for _ in range(self.graph.turns+1)]
        self.debugInfo: bool = debugInfo
        self.deepness: int = deepness
        self.turns: list[list[int]] = []
        self.nbOfNodes = [(stage+1)*self.deepness + 1 for stage in range(self.graph.turns)]

    def construct(self) -> tuple[Node, Node]:
        """Build a linear/log growth tree exploring all path worth of being explored."""
        stage = 0
        print("\nBuilding the tree ...") if self.debugInfo else None

        root: Node = Node(self.graph.startingCell, parent=None, alt=0, sum=0)

        maxLeaf = [root]
        curStage = [root]
        for stage in range(self.graph.turns):
            stageCoveredTarget = self.coveredTarget[stage+1]
            stack = curStage.copy()
            curStage.clear()
            lenCurStage = 0
            for _ in range(len(stack)):
                node = stack.pop()
                for alt in self._directions(node):
                    cell = node.cell.neighbors[alt]
                    if cell is self.graph.outsideCell:
                        continue
                    points = self._pointForNode(cell, stageCoveredTarget) if alt > 0 else 0
                    nextSum = node.sum+points
                    nextNode = None
                    if lenCurStage >= self.nbOfNodes[stage] and nextSum > curStage[-1].sum:
                        curStage.pop()
                        lenCurStage -= 1
                    if lenCurStage < self.nbOfNodes[stage]:
                        nextNode = Node(cell=cell, alt=alt, parent=node, sum=nextSum)
                        # bisect.insort(curStage, nextNode)
                        self.insort_right(curStage, nextNode)
                        lenCurStage += 1
                        if stage == self.graph.turns-1:
                            if nextSum > maxLeaf[0].sum:
                                maxLeaf = [nextNode]
                            elif nextSum == maxLeaf[0].sum:
                                maxLeaf.append(nextNode)
            # print(f"Stage {stage} completed!")
        nodeChoice = randint(0,len(maxLeaf)-1)
        print(f"{len(maxLeaf)} node with the value: {maxLeaf[0].sum}. We choose the number: {nodeChoice}")  if self.debugInfo else None
        return root, maxLeaf[nodeChoice]

    def _directions(self, node: Node) -> tuple[int] | tuple[int, int] | tuple[int, int,int]:
        """Return all move possible at the altitude of the given node"""
        if self.graph.altitudes > node.alt >= 0 and node.alt > 1:
            return (node.alt, node.alt+1, node.alt-1)
        if self.graph.altitudes > node.alt >= 0:
            return (node.alt, node.alt+1)
        if node.alt > 1:
            return (node.alt, node.alt-1)
        return (node.alt,)

    def _pointForNode(self, cell:Cell, stageCoveredTarget: set[TargetCell]) -> int:
        """Compute the number of point for a node"""
        return len(cell.targetsSet - stageCoveredTarget)

    def bestPath(self, maxLeaf: Node) -> deque[Node]:
        """Return the best path of the tree. Use self.construct() to generate leaves"""
        node = maxLeaf
        path  = deque([node])
        while node.parent is not None:
            node = node.parent      # type: ignore
            path.appendleft(node)   # type: ignore
        return path

    def setCoveredTarget(self, path: deque[Node]) -> list[set[TargetCell]]:
        """Add a path in the explored dict, so the nexts paths will not re-compute the same path, i.e some target are now taken"""
        for n, node in enumerate(path):
            self.coveredTarget[n].update(node.cell.targets)    # type: ignore
        return self.coveredTarget

    #Traduction methods
    def pathToMove(self, path: deque[Node]) -> list[int]:
        """Translate a list of node a.k.a path to a list of move"""
        moves = []
        prevAlt = path.popleft().alt if len(path) > 0 else 0
        for node in path:
                dAlt = node.alt - prevAlt
                moves.append(dAlt)
                prevAlt = node.alt
        return moves

    def solveBestPath(self) -> None:
        """Construct a tree find the best path add it to explored and repeat n times where n is the number of balloon"""
        nbPoints = 0
        n = self.graph.ballons
        gs = time()
        for _ in range(n):
            s = time()
            root, maxLeaf = self.construct()
            path = self.bestPath(maxLeaf)
            self.setCoveredTarget(path)
            mv = self.pathToMove(path)
            self.turns.append(mv)
            nbPoints += path[-1].sum
            print(f"Best path with {path[-1].sum} points. Total: {nbPoints} pts. Made in {(time()-s):.2f}s. Step: {_+1}/{n}") if self.debugInfo else ""
        print("_"*50,f"\n\nSome of path: {nbPoints}. Made in {(time()-gs):.2f}s.\n")  if self.debugInfo else None

    def solve(self, balloonIdx: int, turn: int) -> int:
        assert self.graph.ballons > balloonIdx >= 0
        assert self.graph.turns > turn >= 0
        if len(self.turns) == 0:
            self.solveBestPath()
        return self.turns[balloonIdx][turn]

    def insort_right(self, l: list[Node], n: Node):
        lo, hi = 0, len(l)
        s = n.sum
        while lo < hi:
            mid = (lo + hi) // 2
            if s < l[mid].sum:
                hi = mid
            else:
                lo = mid + 1
        l.insert(lo, n)