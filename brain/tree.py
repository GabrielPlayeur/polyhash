
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
        self.root:Node = Node(self.graph.startingCell, alt=0, stage=0, sum=0)
        self.coveredTarget: dict[int, set[TargetCell]] = {}
     
    def construct(self, increaseRate=500) -> None:
        """Build a linear growth tree exploring all path worth of being explored."""
        size = 1
        currentStage = 0        #corresponding the stage of the nextNode not the node itself
        nbOfNodes = lambda stage: stage*increaseRate + 1

        def pushOrForget(p:list, stage:int, node:Node) -> list:
            if len(p) < nbOfNodes(stage):
                heappush(p, node)
            elif node > p[0]:
                heapreplace(p, node)
            return p

        stack = deque()
        nextStagePQueue = [self.root, ]
        print("\nBuilding the tree ...")

        while stack or nextStagePQueue:
            if not stack:
                stack = deque(nextStagePQueue)
                nextStagePQueue.clear()
                currentStage += 1
                if currentStage%5 == 0:
                    nbNode = min(size, nbOfNodes(currentStage))
                    print(f"    | Nodes created on stage {currentStage}: {nbNode} nodes explored, {max(size-nbNode, 0)} nodes aborted")
            
            node = stack.popleft()
            assert node.stage == currentStage-1


            for alt in self._directions(node):
                cell = node.cell.neighbors[alt]
                if cell is self.graph.outsideCell:
                    continue

                #Creating node
                nextNode = Node(cell=cell, alt=alt, stage=node.stage+1, sum=node.sum+node.points)
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
    

    def refresh(self) -> None:
        """Refresh the tree after a path has been chosen"""

        stack = deque([self.root])

        while stack:
            node = stack.popleft()

            exploredAtStage = self.coveredTarget.get(node.stage)
            if exploredAtStage:
                # print([str(s) for s in exploredAtStage])
                for target in node.cell.targets:
                    if target in exploredAtStage:
                        print("has been decr: ", node, end="")
                        node.decrPointAndSum()
                        print("\t->\t", node)
                        self.coveredTarget[node.stage].remove(target)
            

            for child in node.children:
                child.refreshSum(node.sum)
                stack.append(child)

        
    

    def bestPath(self) -> tuple[int, deque[Node]]:
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

            #counting points
            exploredAtStage = self.coveredTarget.get(node.stage)
            if exploredAtStage:
                for target in node.cell.targets:
                    if target in exploredAtStage:
                        node.decrPointAndSum()

            #treatement
            path.append(node)
            i+=1
            if node.isLeave():
                y += 1
                if node.sum > bestScore:
                    bestScore = node.sum
                    best = path.copy()

                    # print("new best road:")
                    # for node in best:
                    #     print("\t"+str(node))
            else:
                for child in reversed(node.children):
                    if exploredAtStage:
                        child.refreshSum(node.sum)
                    queue.append(child)
        
        print(f"\nBest path found with {bestScore} points")
        print(f"{i} node, {y} leave")
        return bestScore, best
    
    def addInCovered(self, path) -> None:
        """Add a path in the explored dict, so the nexts paths will not re-compute the same path, i.e some target are now taken"""
        for n, node in enumerate(path):
            if not self.coveredTarget.get(n):
                self.coveredTarget[n] = set(node.cell.targets)
            else:
                self.coveredTarget[n].update(node.cell.targets)
            # print(f"at {n}: ", node.cell)

    def reset(self) -> None:
        self.root.children = deque()
        self.coveredTarget = {}
    
    def findNBestPath(self) -> tuple[int, deque[deque[Node]]]:
        """Reset the tree and then, construct a new one find the best path add it to explored and repeat n times where n is the number of balloon"""
        bestPaths = deque()
        self.reset()
        self.construct()
        points = 0
        for _ in range(self.graph.ballons):
            p, path = self.bestPath()
            self.addInCovered(path)
            bestPaths.append(path)
            points += p
            # self.refresh()
            print(self.pathToMove(path))
        return points, bestPaths

    #Traduction methods
    def pathToMove(self, path:deque[Node]) -> list[int]:
        """Translate a list of node a.k.a path to a list of move"""
        moves = []
        prevAlt = path.popleft().alt
        for node in path:
                dAlt = node.alt - prevAlt
                moves.append(dAlt)
                prevAlt = node.alt
        
        return moves

    def pathsToResult(self, points:int, paths:deque[deque[Node]]) -> ResultData:
        """Translate lists of node i.e paths to a ResultData conform to generate a solution"""
        moves = []
        for path in paths:
            moves.append(self.pathToMove(path))
        return ResultData(points, moves)
    
    #Automatized resolution
    def solve(self) -> ResultData:
        """Use all the methods of tree to solve a challenge"""
        points, paths = self.findNBestPath()
        print("_"*50,f"\n\nSome of path: {points}\n")
        return self.pathsToResult(points, paths)
    


if __name__ == "__main__":
    name = "d_final"
    name = "a_example"
    name = "b_small"
    name = "c_medium"
    parser = parseChallenge(f'challenges/{name}.in')
    map = CellMap(parser)
    tree = Tree(map)

    from polysolver import stringifySolution, saveSolution
    result = tree.solve()
    saveSolution(f"output/{name}_tree.txt", stringifySolution(result, map.turns))
    
    # tree.construct()
    # _, path = tree.bestPath()
    # print([[str(k)+":"+str(s) for s in v] for k,v in tree.coveredTarget.items()])
    # tree.refresh()
    