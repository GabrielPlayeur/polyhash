from collections import deque
from heapq import heappush, heapreplace
import math
from node import Node
from cellMap import CellMap
from objects import TargetCell

from objects.cell import Cell
from polyparser import parseChallenge
from polysolver import stringifySolution, saveSolution
from simulation import ResultData


class TreeBrain:
    def __init__(self, graph:CellMap, deepness:int, debugInfo=False) -> None:
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
        self.coveredTarget: dict[int, set[TargetCell]] = {}
        self.debugInfo:bool = debugInfo
        self.deepness:int = deepness

    def construct(self) -> list[Node]:
        """Build a linear/log growth tree exploring all path worth of being explored."""
        size = 1
        llen = 0
        stage = 0
        nbOfNodes = lambda stage: stage*self.deepness + 1
        # nbOfNodes = lambda stage: math.log(stage if stage > 2 else 2)*self.deepness
        
        print("\nBuilding the tree ...") if self.debugInfo else None

        def pushOrForget(p:list, stage:int, node:Node) -> list:
            if len(p) < nbOfNodes(stage):
                heappush(p, node)
            elif node > p[0]:
                heapreplace(p, node)
            return p

        root:Node = Node(self.graph.startingCell, parent=None, alt=0, presum=0, points=0)
        stack = deque([root, ])
        nextStagePQueue = []

        while stage < self.graph.turns-1:
            if not stack:
                stack = deque(nextStagePQueue)
                llen += len(nextStagePQueue)
                nextStagePQueue.clear()
                stage += 1

            node = stack.popleft()

            for alt in self._directions(node):
                cell = node.cell.neighbors[alt]
                if cell is self.graph.outsideCell:
                    continue

                points = self._pointForNode(cell, stage+1)
                nextNode = Node(cell=cell, alt=alt, parent=node, presum=node.sum+node.points, points=points)
                node.addChild(nextNode)
                size += 1

                #Adding node
                nextStagePQueue = pushOrForget(nextStagePQueue, stage, nextNode)

        # print(f"%\nTree constructed with {llen} nodes and {size-llen} node aborted") if self.debugInfo else None
        return nextStagePQueue


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
        exploredAtStage = self.coveredTarget.get(stage, set())

        for target in cell.targets:
            if target not in exploredAtStage:
                points += 1
            else:
                exploredAtStage.remove(target)
        # Update coveredTarget after iteration
        self.coveredTarget[stage] = exploredAtStage
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
        self.coveredTarget = {}
        for n, node in enumerate(path):
            self.coveredTarget[n] = set(node.cell.targets)    # type: ignore
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
    
    def solve(self) -> ResultData:
        """Construct a tree find the best path add it to explored and repeat n times where n is the number of balloon"""
        result = ResultData(0, [])
        for _ in range(self.graph.ballons):
            leaves = self.construct()
            path = self.bestPath(leaves)
            self.setCoveredTarget(path)
            mv = self.pathToMove(path)

            result.tracking.append(mv)
            result.nbPoints += path[-1].sum
            print(mv, len(mv))

        print("_"*50,f"\n\nSome of path: {result.nbPoints}\n")  if self.debugInfo else None
        return result

if __name__ == "__main__":
    name = "a_example"
    name = "d_final"
    name = "c_medium"
    name = "b_small"
    parser = parseChallenge(f'challenges/{name}.in')
    graph = CellMap(parser)

    tr = TreeBrain(graph, 100000, debugInfo=True)
    tr.solve()