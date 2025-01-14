from .brainInit import Brain
from collections import deque, defaultdict
from heapq import heappush, heapreplace
from .node import Node
from cellMap import CellMap
from objects import TargetCell, Cell

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
        self.coveredTarget: dict[int, set[TargetCell]] = defaultdict(set)
        self.debugInfo: bool = debugInfo
        self.deepness: int = deepness
        self.turns: list[list[int]] = []
        self.nbOfNodes = [stage*self.deepness + 1 for stage in range(self.graph.turns)]

    def construct(self) -> tuple[Node, Node]:
        """Build a linear/log growth tree exploring all path worth of being explored."""
        stage = 0
        # nbOfNodes = lambda stage: stage*self.deepness + 1
        print("\nBuilding the tree ...") if self.debugInfo else None

        def pushOrForget(p: list, lenP:int, stage:int, node:Node) -> int:
            if lenP < self.nbOfNodes[stage]:
                heappush(p, node)
                return 1
            # elif node > p[0]:
            #     heapreplace(p, node)
            elif node.sum > p[0].sum:
                heapreplace(p, node)
            return 0

        root: Node = Node(self.graph.startingCell, parent=None, alt=0, sum=0)
        stack = deque()

        maxLeaf = root
        curStage = [root]
        while stage < self.graph.turns:
            stageCoveredTarget = self.coveredTarget.get(stage+1, set())
            stack = deque(curStage)
            curStage.clear()
            lenCurStage = 0
            for _ in range(len(stack)):
                node = stack.popleft()
                for alt in self._directions(node):
                    cell = node.cell.neighbors[alt]
                    if cell is self.graph.outsideCell:
                        continue
                    points = self._pointForNode(cell, stageCoveredTarget) if alt > 0 else 0
                    nextNode = Node(cell=cell, alt=alt, parent=node, sum=node.sum+points)
                    if nextNode.sum >= maxLeaf.sum:
                        maxLeaf = nextNode
                    #Adding node
                    # stack.append(nextNode)
                    lenCurStage += pushOrForget(curStage, lenCurStage, stage, nextNode)
            stage += 1
        return root, maxLeaf

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
        print(f"%\nBest path with {path[-1].sum} points") if self.debugInfo else ""
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

    def solveBestPath(self) -> None:
        """Construct a tree find the best path add it to explored and repeat n times where n is the number of balloon"""
        nbPoints = 0
        for _ in range(self.graph.ballons):
            root, maxLeaf = self.construct()
            path = self.bestPath(maxLeaf)
            self.setCoveredTarget(path)
            mv = self.pathToMove(path)
            self.turns.append(mv)
            nbPoints += path[-1].sum
            print(mv, nbPoints, len(mv))
        print("_"*50,f"\n\nSome of path: {nbPoints}\n")  if self.debugInfo else None

    def solve(self, balloonIdx: int, turn: int) -> int:
        assert self.graph.ballons > balloonIdx >= 0
        assert self.graph.turns > turn >= 0
        if len(self.turns) == 0:
            self.solveBestPath()
        return self.turns[balloonIdx][turn]