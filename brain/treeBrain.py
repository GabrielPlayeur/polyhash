from .brainInit import Brain
from collections import deque
from heapq import heappush, heapreplace
from .node import Node
from cellMap import CellMap
from objects import TargetCell, Cell
from time import time
from random import randint

class TreeBrain(Brain):
    """A concrete implementation of the Brain class using a tree-based pathfinding approach.

    This class constructs a decision tree to explore possible movements of a balloon
    and determine the optimal path based on a given environment (graph).
    """

    def __init__(self, graph: CellMap, wideness: int, deepness: int, debugInfo: bool=False) -> None:
        """
        Initialize a Tree instance.

        Args:
            wideness (int):
                The maximum wide to which the tree will be expanded, i.e the coefficeint of the linear increasement
                of the number of nodes explored each stage of the tree.
            deepness (int): The depth of the tree to explore per iteration.
            debugInfo (bool, optional): Flag to enable or disable debug information. If True, additional debug output will be provided during execution. Defaults to False.
        """
        self.graph: CellMap = graph
        self.coveredTarget: list[set[TargetCell]] = [set() for _ in range(self.graph.turns+1)]
        self.debugInfo: bool = debugInfo
        self.wideness: int = wideness
        self.defaultDepth: int = deepness      #the depth of the tree construction: higher value improve performance but reduce result output
        self.turns: list[list[int]] = []
        self.nbOfNodes: list[int] = [(stage+1)*self.wideness for stage in range(self.graph.turns)]

    def construct(self, root: Node, depthS: int, addDepth: int, debug: bool=False) -> Node:
        """Build a linear growth tree exploring all path worth of being explored using insert in list methode (more efficient for small size tree O(n) ).

        Args:
            root (Node): The starting node.
            depthS (int): The starting depth.
            addDepth (int): The additional depth to explore.
            debug (bool, optional): Enable debug prints. Defaults to False.

        Returns:
            Node: The best leaf node found in the constructed tree.
        """
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

    def constructWithHeap(self, root: Node, depthS: int, addDepth: int, debug: bool=False) -> Node:
        """Build a linear growth tree exploring all path worth of being explored using an heap methode (more efficient for large size tree O(logn) ).

        Args:
            root (Node): The starting node.
            depthS (int): The starting depth.
            addDepth (int): The additional depth to explore.
            debug (bool, optional): Enable debug prints. Defaults to False.

        Returns:
            Node: The best leaf node found in the constructed tree.
        """
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
                    if lenCurStage < self.nbOfNodes[localStage]:
                        nextNode = Node(cell=cell, alt=alt, parent=node, sum=nextSum)
                        heappush(curStage, nextNode)
                        lenCurStage += 1
                    elif node.sum > curStage[0].sum:
                        nextNode = Node(cell=cell, alt=alt, parent=node, sum=nextSum)
                        heapreplace(curStage, nextNode)
                    if localStage == addDepth-1 and nextNode is not None:
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
        """Computes the score for a given node based on its cell and altitude."""
        if alt == 0:
            return 0
        return len(cell.targetsSet - stageCoveredTarget)

    def bestPath(self, maxLeaf: Node) -> deque[Node]:
        """Extracts the best path from the constructed tree.

        Args:
            maxLeaf (Node): The leaf node with the best score.

        Returns:
            deque[Node]: The optimal path from root to the best leaf node.
        """
        node = maxLeaf
        path  = deque([node])
        while node.parent is not None:
            node = node.parent      # type: ignore
            path.appendleft(node)   # type: ignore
        return path

    def setCoveredTarget(self, path: deque[Node]) -> list[set[TargetCell]]:
        """Marks targets as covered along a given path."""
        for n, node in enumerate(path):
            self.coveredTarget[n].update(node.cell.targets)    # type: ignore
        return self.coveredTarget

    def pathToMove(self, path: deque[Node]) -> list[int]:
        """Converts a path of nodes into a sequence of moves."""
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
        """Splits the tree depth into manageable chunks for step-wise exploration."""
        depths = []
        for _ in range(self.graph.turns//self.defaultDepth):
            depths.append(self.defaultDepth)
        if rest:=self.graph.turns%self.defaultDepth:
            depths.append(rest)
        return depths

    def solveByStep(self) -> deque[Node]:
        """Constructs the decision tree in stages and determines the best path."""
        root = Node(self.graph.startingCell, parent=None, alt=0, sum=0)
        depths = self.splitDepths()
        print("\nBuilding the splitted tree ...") if self.debugInfo else None
        constructeur = self.construct if self.defaultDepth*self.wideness < 20_000 else self.constructWithHeap
        curDepth = 0
        for n, addDepth in enumerate(depths):
            s = time()
            maxLeaf = constructeur(root, curDepth, addDepth, len(depths)==1)
            if maxLeaf.cell is self.graph.outsideCell:
                return self.bestPath(maxLeaf)
            curDepth += addDepth
            root = maxLeaf
            print(f"\t-Split {n+1}/{len(depths)} in {(time()-s):.2f}s") if self.debugInfo and len(depths) > 1 else None
        return self.bestPath(maxLeaf)

    def solveBestPath(self) -> None:
        """Finds the best path for each balloon and stores the movement instructions."""
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
        """Determine the best move for a balloon at a specific turn using tree search.

        Args:
            balloonIdx (int): The index of the balloon.
            turn (int): The turn number.

        Returns:
            int: The optimal move (-1, 0, or 1).
        """
        assert self.graph.balloons > balloonIdx >= 0
        assert self.graph.turns > turn >= 0
        if len(self.turns) == 0:
            self.solveBestPath()
        return self.turns[balloonIdx][turn]

    def insort_right(self, l: list[Node], n: Node, lo, hi) -> None:
        """Inserts a node into a sorted list while maintaining order."""
        s = n.sum
        while lo < hi:
            mid = (lo + hi) // 2
            if s < l[mid].sum:
                hi = mid
            else:
                lo = mid + 1
        l.insert(lo, n)