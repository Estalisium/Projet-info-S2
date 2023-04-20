import numpy as np
import Planete
import Plateau
import random
import Jeux


class Joueur():
    def __init__(self, id, nom, jeu):
        self.id = id
        self.jeu = jeu
        self.nom = nom
        self.sante = 3
        self.pos = None
        self.cartes = [0, 1, 2, 3, 4]
        self.survie = []
        self.defausse = []

    def lacher_prise(self):
        self.sante = 3
        for carte in self.defausse:
            self.cartes.append(carte)
        self.jeu.traque.avancer()

    def choisir_lieu(self):
        if len(self.cartes) == 0:
            print("vous n'avez plus de cartes en main et devez donc lacher prise")
            self.lacher_prise()
        print("vos cartes sont :", self.cartes)
        val = -1
        while val < 0:
            msg = f"Votre choix de lieu parmi ceux disponible ?\n"
            val = int(input(msg))
            if val in self.cartes:
                self.jeu.board.placer_joueur(val)
                self.pos = val
            else:
                print("Cette carte n'est pas dans votre main veuillez choisir un autre lieu")
                val = -1


class Creature():
    def __init(self, jeu):
        self.jetons = [1]
        self.jeu = jeu

    def placer_jetons(self):
        for jeton in self.jetons:
            pos = random.randint(0, 9)
            self.jeu.board.placer_creature(pos, jeton)


if __name__ == "__main__":
    test = Joueur(1, 'Marie', Jeux.Jeux(1, ['Marie']))
    test.choisir_lieu()
    test.lacher_prise()
    print(test.jeu.board, test.jeu.traque)
