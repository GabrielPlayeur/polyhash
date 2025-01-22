import os
from .brainInit import Brain

class VerifyBrain(Brain):
    """A concrete implementation of the Brain class using predefined moves from a file.

    This class reads a file containing predefined moves for each balloon at each turn 
    and determines the next move based on the file contents.
    """

    def __init__(self, name: str) -> None:
        """Initialize VerifyBrain with the given file name.

        Args:
            name (str): The name of the file containing the predefined moves.
        """
        self.file = name
        self.lines: list[str]
        self.splitLines: dict[int, list[str]] = {}
        self._load()

    def _load(self) -> None:
        """Load the move instructions from the specified file.
        """
        assert os.path.exists(self.file) == True, f"Given file didn't exist: {self.file}"
        with open(self.file, "r") as f:
            self.lines = f.readlines()

    def solve(self, balloonIdx: int, turn: int) -> int:
        """Retrieve the predefined move for the given balloon at the specified turn.

        Args:
            balloonIdx (int): The index of the balloon.
            turn (int): The turn number.

        Returns:
            int: The move (-1, 0, or 1) read from the file.
        """
        assert len(self.lines[0]) > balloonIdx >= 0
        assert len(self.lines) > turn >= 0
        if self.splitLines.get(turn) is None:
            self.splitLines[turn] = self.lines[turn].split()
        return int(self.splitLines[turn][balloonIdx])