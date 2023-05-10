import numpy as np
import Token
import Planete


class Plateau(list):
    """
    Représente le plateau de jeu
    Gère la correspondance entre la position du joueur et la carte lieu associée
    """
    marqueur_vide = 0
    marqueur_creature = 1
    marqueur_artemia = 2
    marqueur_traque = 3

    def __init__(self):
        for i in range(10):
            if i == 0:
                pos = Planete.Antre()
            if i == 1:
                pos = Planete.Jungle()
            if i == 2:
                pos = Planete.Riviere()
            if i == 3:
                pos = Planete.Plage()
            if i == 4:
                pos = Planete.Rover()
            if i == 5:
                pos = Planete.Marais()
            if i == 6:
                pos = Planete.Abri()
            if i == 7:
                pos = Planete.Epave()
            if i == 8:
                pos = Planete.Source()
            if i == 9:
                pos = Planete.Artefact()
            self.append([])
            self[i] = [i, Plateau.marqueur_vide, Plateau.marqueur_vide, pos]

    def placer_joueur(self, pos):
        if pos > 9 or pos < 0:
            raise ValueError
        self[pos][1] += 1

    def activer_lieu(self, joueur, lieu):
        self[lieu][3].effet(joueur)

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
            self[i][1] = Plateau.marqueur_vide
            self[i][2] = Plateau.marqueur_vide

    def voisin(self, lieu):
        if lieu == 0:
            return [1, 5]
        if lieu == 1: 
            return [0, 2, 6]
        if lieu == 2: 
            return [1, 3, 7]
        if lieu == 3: 
            return [2, 4, 8]
        if lieu == 4:
            return [3, 9]
        if lieu == 5: 
            return [0, 6]
        if lieu == 6: 
            return [1, 5, 7]
        if lieu == 7: 
            return [2, 6, 8]
        if lieu == 8: 
            return [3, 7, 9]
        if lieu == 9: 
            return [4, 8]
        
if __name__ == '__main__':
    test = Plateau((10, 3))
    print(test)
    test.placer_joueur(5)
    test.placer_joueur(5)
    test.placer_joueur(3)
    test.placer_creature(5, 2)
    print(test)
