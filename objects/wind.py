
"""Module.
"""

class Wind:
    def __init__(self, dx: int, dy: int) -> None:
        """Entity that describe the wind with a vec"""
        self.vec: tuple[int,int] = (dx,dy)
        self.dx: int = dx
        self.dy: int = dy