import pytest

from brain import TreeBrain
from brain.node import Node
from cellMap import CellMap
from polyparser import parseChallenge


@pytest.fixture
def tree_setup() -> tuple[TreeBrain, CellMap]:
    parser = parseChallenge("./challenges/a_example.in")
    graph = CellMap(parser)
    tree = TreeBrain(graph, 1000)
    return tree, graph

#TODO: fix this
class TestTreeBrain:
    def test_treeBrain_init(self, tree_setup):
        _, tr = tree_setup(100)
        assert isinstance(tr.root, Node)
        assert tr.root.addChild == None
        assert tr.root.sum == 0 and tr.root.points == 0

    def test_treeBrain_construct(self, tree_setup):
        tree, graph = tree_setup

        def choices(alt:int):
            choice = [alt,]
            if graph.altitudes > alt >= 0:
                choice.append(1+alt)
            if alt > 1:
                choice.append(alt-1)
            return choice

        def inner(node):
            if node.stage <= graph.turns:
                for choice in choices(node.alt):
                    newnode = Node(node.cell.getNeighbor(choice), choice, node.stage+1, node.sum, len(node.cell.targets))
                    node.addChild(newnode)
                    inner(newnode)
        
        rootImage = Node(graph.startingCell, alt=0, stage=0, presum=0, points=0)
        inner(rootImage)

        tree.construct()
        stack = [tree.root, ]
        stackImage = [rootImage, ]
        while stack:
            node = stack.pop(0)
            nodeImage = stackImage.pop(0)
            assert node == nodeImage
            
            for n in range(len(nodeImage.children)):
                assert len(node.children) > n
                assert nodeImage.children[n] == node.children[n]
                stack.append(node.children[n])
                stackImage.append(nodeImage.children[n])