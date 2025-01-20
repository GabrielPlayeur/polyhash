import random
from .brainInit import Brain, Balloon

class RandomBrain(Brain):
    """A concrete implementation of the Brain class using random movement.

    This class selects a random move for the balloon within its altitude constraints.
    """

    def solve(self, balloon: Balloon) -> int:
        """Determine the next move for a balloon randomly.

        Returns:
            int: A randomly chosen move (-1, 0, or 1) within altitude limits.
        """
        choiceAct: list[int] = [0]
        if balloon.alt - 1 > 0:
            choiceAct.append(-1)
        if balloon.alt + 1 <= balloon.altMax:
            choiceAct.append(1)
        return random.choice(choiceAct)