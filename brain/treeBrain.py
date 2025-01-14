from .brainInit import Brain
from collections import deque, defaultdict
from heapq import heappush, heapreplace, nsmallest
from .node import Node
from cellMap import CellMap
from objects import TargetCell, Cell
import bisect
from time import time
from random import randint

class TreeBrain(Brain):
    def __init__(self, graph: CellMap, wideness: int, deepness: int, debugInfo=False) -> None:
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
        self.coveredTarget: dict[int, set[TargetCell]] = defaultdict(set)
        self.debugInfo: bool = debugInfo
        self.wideness: int = wideness
        self.defaultDepth: int = deepness      #the depth of the tree construction: higher value improve performance but reduce result output
        self.turns: list[list[int]] = []
        self.nbOfNodes = [(stage+1)*self.wideness + 1 for stage in range(self.graph.turns)]

    def construct(self, root: Node, depth: int) -> tuple[Node, Node]:
        """Build a linear/log growth tree exploring all path worth of being explored."""
        stage = 0
        print("\nBuilding the tree ...") if self.debugInfo else None

        stack = deque()

        maxLeaf = [root]
        curStage = [root]
        for stage in range(depth):
            stageCoveredTarget = self.coveredTarget.get(stage+1, set())
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
                        bisect.insort(curStage, nextNode)
                        lenCurStage += 1
                        if stage == depth-1:
                            if nextSum > maxLeaf[0].sum:
                                maxLeaf = [nextNode]
                            elif nextSum == maxLeaf[0].sum:
                                maxLeaf.append(nextNode)
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
        points = 0
        for target in cell.targets:
            if target not in stageCoveredTarget:
                points += 1
        return points

    def bestPath(self, maxLeaf: Node) -> deque[Node]:
        """Return the best path of the tree. Use self.construct() to generate leaves"""
        node = maxLeaf
        path  = deque([node])
        while node.hasParent():     # type: ignore
            node = node.parent      # type: ignore
            path.appendleft(node)   # type: ignore
        return path

    def setCoveredTarget(self, path: deque[Node]) -> dict[int, set[TargetCell]]:
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
        path = deque()
        depths = self.splitDepths()
        debugInfo = self.debugInfo 
        if len(depths) > 1:
            print("Building the splitted tree ...") if self.debugInfo else None

        for n, curDepth in enumerate(depths):
            s = time()
            if len(depths) > 1:self.debugInfo = False
            _, maxLeaf = self.construct(root, curDepth)
            path.extend(self.bestPath(maxLeaf))
            
            root = Node(maxLeaf.cell, maxLeaf.alt, None, sum=maxLeaf.sum)

            self.debugInfo = debugInfo
            print(f"\t-Split {n+1}/{len(depths)} in {(time()-s):.2f}s") if self.debugInfo else None

        return path


    def solveBestPath(self) -> None:
        """Construct a tree find the best path add it to explored and repeat n times where n is the number of balloon"""
        nbPoints = 0
        n = self.graph.ballons
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
        assert self.graph.ballons > balloonIdx >= 0
        assert self.graph.turns > turn >= 0
        if len(self.turns) == 0:
            self.solveBestPath()
        return self.turns[balloonIdx][turn]