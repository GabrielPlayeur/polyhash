import os
from .brainInit import Brain

class VerifyBrain(Brain):
    def __init__(self, name: str) -> None:
        self.file = name
        self.lines: list[str]
        self.splitLines: dict[int, list[str]] = {}
        self._load()

    def _load(self):
        assert os.path.exists(self.file)==True, f"Given file didn't exist: {self.file}"
        with open(self.file, "r") as f:
            self.lines = f.readlines()

    def solve(self, balloonIdx: int, turn: int) -> int:
        assert len(self.lines[0]) > balloonIdx >= 0
        assert len(self.lines) > turn >= 0
        if self.splitLines.get(turn) is None:
            self.splitLines[turn] = self.lines[turn].split()
        return int(self.splitLines[turn][balloonIdx])