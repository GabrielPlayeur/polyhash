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
        self.graph:CellMap = graph
        self.coveredTarget: dict[int, set[TargetCell]] = defaultdict(set)
        self.debugInfo:bool = debugInfo
        self.deepness:int = deepness
        self.turns: list[list[int]] = []

    def construct(self) -> tuple[Node, list[Node]]:
        """Build a linear/log growth tree exploring all path worth of being explored."""
        size = 1
        llen = 0
        stage = 0
        nbOfNodes = lambda stage: stage*self.deepness + 1
        # nbOfNodes = lambda stage: math.log(stage if stage > 2 else 2)*self.deepness
        print("\nBuilding the tree ...") if self.debugInfo else None

        def pushOrForget(p:list, stage:int, node:Node) -> None:
            if len(p) < nbOfNodes(stage):
                heappush(p, node)
            elif node > p[0]:
                heapreplace(p, node)

        root: Node = Node(self.graph.startingCell, parent=None, alt=0, presum=0, points=0)
        stack = deque([root, ])

        while stage < self.graph.turns:
            for _ in range(len(stack)):
                node = stack.popleft()
                for alt in self._directions(node):
                    cell = node.cell.neighbors[alt]
                    if cell is self.graph.outsideCell:
                        continue
                    points = self._pointForNode(cell, stage+1) #TODO: fix this
                    nextNode = Node(cell=cell, alt=alt, parent=node, presum=node.sum, points=points)
                    node.addChild(nextNode)
                    size += 1
                    #Adding node
                    stack.append(nextNode)
                    # pushOrForget(leafs, stage, nextNode)
            stage += 1
        # print(f"%\nTree constructed with {llen} nodes and {size-llen} node aborted") if self.debugInfo else None
        return root, list(stack)

    def _directions(self, node:Node) -> list[int]:
        """Return all move possible at the altitude of the given node"""
        choice = [node.alt,]
        if self.graph.altitudes > node.alt >= 0:
            choice.append(1+node.alt)
        if node.alt > 1:
            choice.append(node.alt-1)
        return choice

    def _pointForNode(self, cell:Cell, stage:int) -> int:
        """Compute the number of point for a node"""
        points = 0
        for target in cell.targets:
            if target not in self.coveredTarget.get(stage, set()):
                points += 1
        return points

    def bestPath(self, leaves:list[Node]) -> deque[Node]:
        """Return the best path of the tree. Use self.construct() to generate leaves"""
        # take the best leaf with largest sum
        node = max(leaves, key=lambda x: x.sum)
        path  = deque([node])
        while node.hasParent():     # type: ignore
            node = node.parent      # type: ignore
            path.appendleft(node)   # type: ignore
        print(f"%\nBest path with {path[-1].sum} points") if self.debugInfo else ""
        return path

    def setCoveredTarget(self, path:deque[Node]) -> dict[int, set[TargetCell]]:
        """Add a path in the explored dict, so the nexts paths will not re-compute the same path, i.e some target are now taken"""
        for n, node in enumerate(path):
            self.coveredTarget[n].update(set(node.cell.targets))    # type: ignore TODO: optimize
        return self.coveredTarget

    #Traduction methods
    def pathToMove(self, path:deque[Node]) -> list[int]:
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
            root, leaves = self.construct()
            path = self.bestPath(leaves)
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