

from node import Node
from cellMap import CellMap
from polyparser import parseChallenge
from simulation import Simulation


class Tree:
    def __init__(self, graph:CellMap) -> None:
        self.graph:CellMap = graph
        self.root:Node = Node(self.graph.startingCell, alt=0, stage=0, sum=0)
     
    def construct(self) -> None:
            """Build a tree exploring all path worth of being explored."""
            size, goingOut = 0, 0
            mod = 0
            stack = [self.root, ]
            while stack:
                node = stack.pop(0)

                if not self._isWorth(node):
                    continue

                for alt in self._directionChoices(node):
                    cell = node.cell.neighbors[alt]
                    if cell is self.graph.outsideCell:
                        goingOut += 1
                        continue
                    nextNode = Node(cell, alt, node.stage+1, node.sum+node.points)
                    node.addSon(nextNode)
                    size += 1

                    if nextNode.stage < self.graph.turns:
                        stack.append(nextNode)
                
                if size//100_000 > mod:
                    mod += 1
                    print(f"{size} nodes has been created with {goingOut} path aborted...")
            
            print(f"Tree constructed with {size} nodes")


    def _directionChoices(self, node:Node) -> list[int]:
        """Return all altitude move possible"""
        choice = [node.alt,]

        if self.graph.altitudes > node.alt >= 0:
            choice.append(1+node.alt)
        if node.alt > 1:
            choice.append(node.alt-1)

        return choice


    def _isWorth(self, node:Node) -> bool:
        return int(node.stage*0.3) <= node.sum
    
    def bestPath(self) -> list[Node]:
        explored = set()
        path = []
        best = []
        bestScore = 0
        
        node = self.root

        def goUp(path, explored) -> Node:
            node = path.pop()
            """
            if not node.isLeave():
                for child in node.
            """
            explored.add(node)
            return path.pop()

        def goDown(path, explored) -> Node:
            node = path[-1]
            n = 0
            while n < len(node.children) and node.children[n] in explored:
                n += 1
            
            if n >= len(node.children):
                return goUp(path, explored)
            else:
                return node.children[n]

        
        while self.root not in explored:
            if node.isLeave():
                if path[-1].sum > bestScore:
                    bestScore = path[-1].sum
                    best = path[:]              #saving best path
                explored.add(node)

            if node in explored:
                node = goUp(path, explored)
            else:
                node = goDown(path, explored)

        return best

        
                

if __name__ == "__main__":
    name = "c_medium"
    name = "b_small"
    parser = parseChallenge(f'challenges/{name}.in')
    map = CellMap(parser)
    tree = Tree(map)
    print(tree.bestPath())
    tree.construct()