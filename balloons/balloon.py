
"""Module.
"""
from cells import Cell

class Balloon:
    def __init__(self) -> None:
        self.cell: Cell
        self.alt: int

    def moveAlt(self) -> None:
        raise NotImplementedError