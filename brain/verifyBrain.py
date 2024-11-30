from .brainInit import Brain, Balloon


class VerifyBrain(Brain):
    def __init__(self, fileName):
        assert fileName is not None
        self.lines: list[str]
        self.fileName:str = fileName
        self._load()

    def _load(self):
        with open(self.fileName, "r") as f:
            self.lines = f.readlines()

    def solve(self, baloonIdx, turn) -> int:
        return int(self.lines[turn].split()[baloonIdx])