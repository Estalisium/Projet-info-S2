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
        self.cartes = [0,1,2,3,4]
        self.survie = []
        self.useCard = 1
        self.River = False
        self.Artefact = False
        self.posArtefact = None
        self.posRiver = None
        self.defausse = []
        self.esquive = 0

    def pick(self):
        self.survie.append(self.jeu.DeckSurvie.draw())

    def jouerCarte(self, phase):
        if self.useCard > 0:
            for carte in self.survie:
                if carte.phase == phase:
                    msg = f"Voulez vous jouer la carte {carte}?\n{carte.description()}\nOui : 0, Non : 1\n>> "
                    val = int(input(msg))
                    if val == 0:
                        carte.effet(self)

    def __str__(self):
        return 'Joueur ' + str(self.id) + ' : ' + self.nom

    def reprendre_toute_defausse(self):
        for carte in self.defausse:
            self.cartes.append(carte)
            self.cartes.sort()
        self.defausse = []

    def lacher_prise(self):
        print(self, 'lache prise')
        self.sante = 3
        self.reprendre_toute_defausse()
        self.jeu.traque.avancer()

    def __repr__(self):
        return 'Joueur ' + str(self.id) + ' : ' + self.nom

    def choisir_lieu(self):
        if len(self.cartes) == 0:
            print("Vous n'avez plus de cartes en main et devez donc lacher prise")
            self.lacher_prise()
        print("Vos lieux en main sont : ", self.cartes)
        val = -1
        while val < 0:
            msg = f"Votre choix de lieu parmi ceux disponible ?\n >> "
            val = int(input(msg))
            if val in self.cartes:
                self.jeu.board.placer_joueur(val)
                self.pos = val
            else:
                print("Cette carte n'est pas dans votre main veuillez choisir un autre lieu")
                val = -1
        if self.River or self.Artefact:
            carteRiver = self.cartes.copy()
            carteRiver.remove(self.pos)
            print("La rivière est active, veuillez choisir un deuxième Lieu")
            if len(self.cartes) == 0:
                print("Vous n'avez plus de cartes en main et devez donc lacher prise")
                self.lacher_prise()
            print("Vos lieux en main sont : ", carteRiver)
            val = -1
            while val < 0:
                msg = f"Votre choix de lieu parmi ceux disponible ?\n >> "
                val = int(input(msg))
                if val in self.cartes:
                    self.jeu.board.placer_joueur(val)
                    self.posRiver = val
                else:
                    print("Cette carte n'est pas dans votre main veuillez choisir un autre lieu")
                    val = -1

    def reprendreDefausse(self):
        print("Vos lieux défaussés sont : ", self.defausse)
        if len(self.defausse) <= 0:
            print('Votre défausse est vide, il ne se passe rien')
            return 1
        val = -1
        while val < 0:
            msg = f"Lequel voulez vous reprendre en main?\n >> "
            val = int(input(msg))
            if val in self.defausse:
                self.defausse.remove(val)
                self.cartes.append(val)
                self.cartes.sort()
            else:
                print("Ce lieu n'est pas dans votre défausse veuillez en choisir un autre")
                val = -1

    def creature(self):
        if self.esquive == 1:
            self.esquive = 0
            print("Jeton créature évité")
            return 1
        else:
            if self.pos == 0:
                self.sante -= 2
            else:
                self.sante -= 1
            if self.jeu.creature.eat == 0:
                self.jeu.creature.eat = 1
                self.jeu.traque.avancer()
            if self.sante <= 0:
                self.lacher_prise()

    def artemia(self):
        if self.esquive == 1:
            self.esquive = 0
            print("Jeton artemia évité")
            return 1
        else:
            self.defausseCarte(1)
            self.defausseCarte(1)

    def defausseCarte(self, mode):
        """
        Permet de défausser une carte,
        :param mode: int, permet de préciser si c'est une défausse libre ou la défausse forcée en fin de phase 4
        """
        if mode == 0:
            if self.esquive == 1:
                print('Vous reprenez en main votre carte lieu')
                self.esquive = 0
            else:
                self.defausse.append(self.pos)
                self.cartes.remove(self.pos)
        elif mode == 1:
            print("Vos lieux en main sont : ", self.defausse)
            val = -1
            while val < 0:
                msg = f"Lequel voulez vous défausser?\n >> "
                val = int(input(msg))
                if val in self.cartes:
                    self.cartes.remove(val)
                    self.defausse.append(val)
                else:
                    print("Ce lieu n'est pas dans votre main veuillez en choisir un autre")
                    val = -1


class Creature():
    def __init__(self, id, nom, jeu):
        self.id = id
        self.nom = nom
        self.jetons = [1]
        self.useCard = 1
        self.traque = []
        self.jeu = jeu
        self.eat = 0
        self.artemia = None
        self.pos = None

    def CaraJeton(self, jeton):
        if jeton == 1:
            return 'Créature'
        if jeton == 2:
            return 'Artémia'
        if jeton == 3:
            return 'Traque'

    def placer_jetons(self):
        for jeton in self.jetons:
            val = -1
            while val < 0:
                print("Vous avez un jeton " + self.CaraJeton(jeton))
                print('Voici la défausse des joueurs')
                for player in self.jeu.players:
                    print(player, player.defausse)
                msg = f"Où voulez vous le placer ?\n >> "
                val = int(input(msg))
                if -1 < val < 9:
                    if jeton == 1:
                        self.pos = val
                    if jeton == 2:
                        self.artemia = val
                    self.jeu.board.placer_creature(val, jeton)
                else:
                    print('Veuillez saisir un lieu valide')
                    val = -1


if __name__ == "__main__":
    test = Joueur(1, 'Marie', Jeux.Jeux(2, ['Marie', 'test']))
    print(test)
    test.artemia()
    test.reprendreDefausse()
    test.lacher_prise()
    print(test.jeu.board, test.jeu.traque)
