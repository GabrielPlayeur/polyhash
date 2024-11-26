
"""Module.
"""

class Wind:
    def __init__(self, dRow: int, dCol: int) -> None:
        """Entitcol that describe the wind with a vec"""
        self.vec: tuple[int,int] = (dRow,dCol)
        self.dRow: int = dRow
        self.dCol: int = dCol