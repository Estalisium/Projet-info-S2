import numpy as np
import Token


class Plateau(np.ndarray):
    marqueur_vide = 0
    marqueur_creature = 1
    marqueur_artemia = 2
    marqueur_traque = 3

    def __init__(self, shape):
        for i in range(10):
            self[i] = np.array([i, Plateau.marqueur_vide, Plateau.marqueur_vide])

    def placer_joueur(self, pos):
        if pos > 9:
            raise ValueError
        for i in range(10):
            if i == pos:
                self[i][1] += 1

    def placer_creature(self, pos, type):
        """
        :type type: int, marqueur_creature = 1, marqueur_artemia = 2, marqueur_traque = 3,
        :type pos: int
        """
        if pos > 9 or pos < 0:
            raise ValueError
        for i in range(10):
            if i == pos:
                self[i][2] = type

    def reset(self):
        for i in range(10):
            self[i] = np.array([i, Plateau.marqueur_vide, Plateau.marqueur_vide])


if __name__ == '__main__':
    test = Plateau((10, 3))
    print(test)
    test.placer_joueur(5)
    test.placer_joueur(5)
    test.placer_joueur(3)
    test.placer_creature(5, 2)
    print(test)
