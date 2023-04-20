import numpy as np
import Token


class Plateau(np.ndarray):
    marqueur_vide = 0
    marqueur_creature = 1
    marqueur_artemia = 2
    marqueur_traque = 3

    def __init__(self, shape):
        for i in range(10):
            if i < 5:
                self[0][i % 5] = np.array([i, Plateau.marqueur_vide, Plateau.marqueur_vide])
            else:
                self[1][i % 5] = np.array([i, Plateau.marqueur_vide, Plateau.marqueur_vide])

    def placer_joueur(self, pos):
        if pos > 9:
            raise ValueError
        test = 0
        i = 0
        while test == 0:
            if i < 5:
                if self[0][i % 5][0] == pos:
                    self[0][i % 5][1] += 1
                    test = 1
            else:
                if self[1][i % 5][0] == pos:
                    self[1][i % 5][1] += 1
                    test = 1
            i += 1

    def placer_creature(self, pos, type):
        if pos > 9:
            raise ValueError
        test = 0
        i = 0
        while test == 0:
            if i < 5:
                if self[0][i % 5][0] == pos:
                    self[0][i % 5][2] = type
                    test = 1
            else:
                if self[1][i % 5][0] == pos:
                    self[1][i % 5][2] = type
                    test = 1
            i += 1



if __name__ == '__main__':
    test = Plateau((2, 5, 3))
    print(test)
    test.placer_joueur(5)
    test.placer_joueur(5)
    test.placer_joueur(3)
    print(test)
