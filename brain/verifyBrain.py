from .brainInit import Brain, Balloon


class VerifyBrain(Brain):
    def __init__(self):
        self.file = "d_sol.txt"

    def solve(self, baloonIdx, turn) -> int:
        with open(self.file, "r") as f:
            lines = f.readlines()
            return int(lines[turn].split()[baloonIdx])
        


brain = VerifyBrain()