"""
Module for simulating the behavior of a Wind object.

This module defines a Wind class that represents the wind's direction and magnitude in a 2D grid.
The wind is described by a vector with row and column changes, which indicates its direction and strength.
"""

class Wind:
    def __init__(self, dRow: int, dCol: int) -> None:
        """Entitcol that describe the wind with a vec"""
        self.vec: tuple[int,int] = (dRow,dCol)
        self.dRow: int = dRow
        self.dCol: int = dCol