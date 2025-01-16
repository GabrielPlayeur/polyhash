from .brainInit import Brain
from collections import deque
from .node import Node
from cellMap import CellMap
from objects import TargetCell, Cell
from time import time
from random import randint

#TODO: add doc
class TreeBrain(Brain):
    def __init__(self, graph: CellMap, wideness: int, deepness: int, debugInfo: bool=False) -> None:
        """
        Initialize a Tree instance.
            -> There two majors ways of using this class:
            - by creating unique Tree and refreshing itself every iteration (very bugged but optimized)
            - by creating a new Tree every iteration and passing it the new coveredTarget argument with a context manager to limit the memory impact (not opti but sure)

        Args:
            `graph` (CellMap):
                The graph representation of the environment, which serves as the base for constructing the tree.

            `wideness` (int): 
                The maximum wide to which the tree will be expanded, i.e the coefficeint of the linear increasement
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
        self.wideness: int = wideness
        self.defaultDepth: int = deepness      #the depth of the tree construction: higher value improve performance but reduce result output
        self.turns: list[list[int]] = []
        self.nbOfNodes: list[int] = [(stage+1)*self.wideness for stage in range(self.graph.turns)]

    def construct(self, root: Node, depthS: int, addDepth: int, debug: bool=False) -> Node:
        """Build a linear/log growth tree exploring all path worth of being explored."""
        maxLeaf: list[Node] = []
        lenMaxLeaf: int = 0 
        curStage: list[Node] = [root]
        for localStage in range(addDepth):
            stageCoveredTarget: set[TargetCell] = self.coveredTarget[localStage+depthS+1]
            stack: list[Node] = curStage.copy()
            curStage.clear()
            lenCurStage: int = 0
            for _ in range(len(stack)):
                node: Node = stack.pop()
                for alt in self._directions(node):
                    cell: Cell = node.cell.neighbors[alt]
                    if cell is self.graph.outsideCell:
                        continue
                    nextSum: int = node.sum + self._pointForNode(alt, cell, stageCoveredTarget)
                    nextNode: Node|None = None
                    if lenCurStage >= self.nbOfNodes[localStage] and nextSum > curStage[-1].sum:
                        curStage.pop()
                        lenCurStage -= 1
                    if lenCurStage < self.nbOfNodes[localStage]:
                        nextNode = Node(cell=cell, alt=alt, parent=node, sum=nextSum)
                        self.insort_right(curStage, nextNode, 0, lenCurStage)
                        lenCurStage += 1
                        if localStage == addDepth-1:
                            if lenMaxLeaf == 0 or nextSum > maxLeaf[0].sum:
                                maxLeaf = [nextNode]
                                lenMaxLeaf = 1
                            elif nextSum == maxLeaf[0].sum:
                                maxLeaf.append(nextNode)
                                lenMaxLeaf += 1
            # print(f"Stage {localStage} completed!")
        if lenMaxLeaf == 0:
            return Node(self.graph.outsideCell, root.alt, root, root.sum)
        nodeChoice = randint(0,lenMaxLeaf-1)
        print(f"{lenMaxLeaf} node with the value: {maxLeaf[0].sum}. We choose the number: {nodeChoice}") if debug else None
        return maxLeaf[nodeChoice]

    def _directions(self, node: Node) -> tuple[int] | tuple[int, int] | tuple[int, int,int]:
        """Return all move possible at the altitude of the given node"""
        if self.graph.altitudes > node.alt > 1:
            return (node.alt, node.alt+1, node.alt-1)
        if node.alt <= 1:
            return (node.alt, node.alt+1)
        if node.alt == self.graph.altitudes:
            return (node.alt, node.alt-1)
        raise ValueError('Cannot move with the given Node')

    def _pointForNode(self, alt: int, cell: Cell, stageCoveredTarget: set[TargetCell]) -> int:
        """Compute the number of point for a node"""
        if alt == 0:
            return 0
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

    def pathToMove(self, path: deque[Node]) -> list[int]:
        """Translate a list of node a.k.a path to a list of move"""
        moves = []
        prevAlt = path.popleft().alt if len(path) > 0 else 0
        for node in path:
            dAlt = node.alt - prevAlt
            if dAlt < -1 or dAlt > 1:
                print(dAlt, node.alt, prevAlt)
                raise ValueError
            moves.append(dAlt)
            prevAlt = node.alt
        for _ in range(self.graph.turns-len(moves)):
            moves.append(0)
        return moves

    def splitDepths(self) -> list[int]:
        depths = []
        for _ in range(self.graph.turns//self.defaultDepth):
            depths.append(self.defaultDepth)
        if rest:=self.graph.turns%self.defaultDepth:
            depths.append(rest)
        return depths

    def solveByStep(self) -> deque[Node]:
        """the method to split the tree's construction and the bestPath finding"""
        root = Node(self.graph.startingCell, parent=None, alt=0, sum=0)
        depths = self.splitDepths()
        print("\nBuilding the splitted tree ...") if self.debugInfo else None
        curDepth = 0
        for n, addDepth in enumerate(depths):
            s = time()
            maxLeaf = self.construct(root, curDepth, addDepth, len(depths)==1)
            if maxLeaf.cell is self.graph.outsideCell:
                return self.bestPath(maxLeaf)
            curDepth += addDepth
            root = maxLeaf
            print(f"\t-Split {n+1}/{len(depths)} in {(time()-s):.2f}s") if self.debugInfo and len(depths) > 1 else None
        return self.bestPath(maxLeaf)

    def solveBestPath(self) -> None:
        """Construct a tree find the best path add it to explored and repeat n times where n is the number of balloon"""
        nbPoints = 0
        n = self.graph.balloons
        gs = time()
        for cur in range(n):
            s = time()
            path = self.solveByStep()
            self.setCoveredTarget(path)
            mv = self.pathToMove(path)
            self.turns.append(mv)
            nbPoints += path[-1].sum
            print(f"Best path with {path[-1].sum} points. Total: {nbPoints} pts. Made in {(time()-s):.2f}s. Step: {cur+1}/{n}") if self.debugInfo else ""
        print("_"*50,f"\n\nSome of path: {nbPoints}. Made in {(time()-gs):.2f}s.\n")  if self.debugInfo else None

    def solve(self, balloonIdx: int, turn: int) -> int:
        assert self.graph.balloons > balloonIdx >= 0
        assert self.graph.turns > turn >= 0
        if len(self.turns) == 0:
            self.solveBestPath()
        return self.turns[balloonIdx][turn]

    def insort_right(self, l: list[Node], n: Node, lo, hi) -> None:
        """With our profiling, it turns out that insertion in a list is better than maintaining a minheap when the list is small ;)"""
        s = n.sum
        while lo < hi:
            mid = (lo + hi) // 2
            if s < l[mid].sum:
                hi = mid
            else:
                lo = mid + 1
        l.insert(lo, n)