from .brainInit import Brain, Balloon


class VerifyBrain(Brain):
    def __init__(self, name):
        self.file = name
        self.lines: list[str]
        self.splitLines: dict[str, list[str]] = {}
        self._load()

    def _load(self):
        with open(self.file, "r") as f:
            self.lines = f.readlines()

    def solve(self, baloonIdx, turn) -> int:
        if self.splitLines.get(turn) is None:
            self.splitLines[turn] = self.lines[turn].split()
        return int(self.splitLines[turn][baloonIdx])