
from collections import deque
from heapq import heappush, heapreplace
from node import Node
from cellMap import CellMap
from objects import TargetCell
from polyparser import parseChallenge
from simulation import ResultData


class Tree:
    def __init__(self, graph:CellMap) -> None:
        self.graph:CellMap = graph
        self.root:Node = Node(self.graph.startingCell, alt=0, stage=0, sum=0, points=0)
        self.explored: dict[int, set[TargetCell]] = {}
     
    def construct(self, increaseRate=30) -> None:
        """Build a linear growth tree exploring all path worth of being explored."""
        size = 1
        currentStage = 0
        nbOfNodes = lambda stage: stage*increaseRate + 1

        def pushOrForget(p:list, stage:int, node:Node) -> list:
            if len(p) < nbOfNodes(stage):
                heappush(p, node)
            elif node > p[0]:
                heapreplace(p, node)
            return p

        stack = deque()
        nextStagePQueue = [self.root, ]

        while stack or nextStagePQueue:
            if not stack:
                stack = deque(nextStagePQueue)
                nextStagePQueue.clear()
                currentStage += 1
                if currentStage%5 == 0:
                    nbNode = min(size, nbOfNodes(currentStage))
                    print(f"Nodes created on stage {currentStage}: {nbNode} nodes explored, {max(size-nbNode, 0)} nodes aborted")
            
            node = stack.popleft()


            for alt in self._directions(node):
                cell = node.cell.neighbors[alt]
                if cell is self.graph.outsideCell:
                    continue

                #Counting points
                if self.explored and cell.targets and self.explored.get(node.stage+1):
                    points = 0
                    for target in cell.targets:
                        if target in self.explored[node.stage+1]:
                            points += 1
                else:
                    points = len(cell.targets)
                nextNode = Node(cell=cell, alt=alt, stage=node.stage+1, sum=node.sum+node.points, points=points)
                node.addChild(nextNode)
                size += 1

                if nextNode.stage < self.graph.turns:
                    nextStagePQueue = pushOrForget(nextStagePQueue, currentStage, nextNode)
                else:
                    #is a leave
                    #print(node.alt, node.sum)
                    pass
            
        print(f"Tree constructed with {min(size, nbOfNodes(currentStage))} nodes")


    def _directions(self, node:Node) -> list[int]:
        """Return all move possible at the altitude of the given node"""
        choice = [node.alt,]

        if self.graph.altitudes > node.alt >= 0:
            choice.append(1+node.alt)
        if node.alt > 1:
            choice.append(node.alt-1)

        return choice
    

    def bestPath(self) -> deque[Node]:
        """Browse the tree to find the best path. Once the path is done being computed it's added to the explored dict"""
        path:deque[Node] = deque()
        best = deque()
        bestScore = 0
        
        queue = deque([self.root,])
        i, y = 0, 0
        while queue:
            node = queue.pop()

            #refreshing path
            while path and node not in path[-1].children:
                path.pop()

            #treatement
            path.append(node)
            i+=1
            if node.isLeave():
                y += 1
                if node.sum >= bestScore:
                    bestScore = node.sum
                    best = path.copy()

                    for node in best:
                        assert 0 <= node.alt <= self.graph.altitudes
            else:
                for child in reversed(node.children):
                    queue.append(child)
        
        best.popleft() #Remove the useless first node
        print(f"\nBest path found with {bestScore} points")
        print(f"{i} node, {y} leave")
        self._addInExplored(path=best)
        return best
    
    def findNBestPath(self, n:int) -> deque[deque[Node]]:
        """Reset the tree and then, construct a new one find the best path add it to explored and repeat n times"""
        bestPaths = deque()
        self.reset()
        for _ in range(n):
            self.construct()
            path = self.bestPath()
            bestPaths.append(path)
        self.reset()
        return bestPaths

    def reset(self) -> None:
        self.root.children = deque()
        self.explored = {}
    
    def _addInExplored(self, path) -> None:
        """Add a path in the explored dict, so the nexts paths will not re-compute the same path, i.e some target are now taken"""
        for n, node in enumerate(path):
            if not self.explored.get(n):
                self.explored[n] = {node.cell}
            else:
                self.explored[n].add(node.cell)


    def pathToMove(self, path:deque[Node]) -> list[int]:
        """Translate a list of node a.k.a a path to a list of move"""
        moves = []
        prevAlt = 0
        for node in path:
                dAlt = node.alt - prevAlt
                moves.append(dAlt)
                prevAlt = node.alt
        
        return moves

    def pathsToResult(self, paths:list[deque[Node]]) -> ResultData:
        """Translate lists of node aka paths to a ResultData conform to generate a solution"""
        #TODO: make this method
        return ResultData(0, [[]])


if __name__ == "__main__":
    name = "c_medium"
    name = "d_final"
    name = "a_example"
    name = "b_small"
    parser = parseChallenge(f'challenges/{name}.in')
    map = CellMap(parser)
    tree = Tree(map)
    tree.construct()
    path = tree.bestPath()
    print(len(path), tree.pathToMove(path))