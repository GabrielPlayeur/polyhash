
"""Module.
"""

class Wind:
    def __init__(self, dx: int, dy: int) -> None:
        self.vec: tuple[int,int]
        self.dx: int
        self.dy: int