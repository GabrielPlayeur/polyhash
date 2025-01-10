import random
from .brainInit import Brain, Balloon

#TODO: add doc
class RandomBrain(Brain):
    def solve(self, balloon: Balloon) -> int:
        choiceAct = [0]
        if balloon.alt-1>0:
            choiceAct.append(-1)
        if balloon.alt+1<=balloon.altMax:
            choiceAct.append(1)
        return random.choice(choiceAct)