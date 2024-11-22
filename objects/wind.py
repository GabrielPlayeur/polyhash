
"""Module.
"""

class Wind:
    def __init__(self, dx: int, dy: int) -> None:
        self.vec: tuple[int,int] = (dx,dy)
        self.dx: int = dx
        self.dy: int = dy