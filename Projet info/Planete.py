import numpy as np
from numpy.random import randint
import sys
import sqlite3
from abc import ABC, abstractmethod
from PyQt5 import QtGui, QtCore, QtWidgets, uic
# from dprint import dprint
import random


class Deck(ABC):
    """
    Classe regroupant tous les types de cartes.
    Classe abstraite, il n'existe que des cartes spécifiques
    surtout utile pour l'IHM
    """

    def __init__(self, type):
        self.type = type
        self.cards = [1, 2, 3, 4]
        self.discard = []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            print("Il n'y a plus de cartes dans le deck, la défausse a été mélangée")
            self.reset()
        draw = self.cards.pop(0)
        self.discard.append(draw)
        return draw

    def reset(self):
        self.cards = self.discard.copy()
        random.shuffle(self.cards)
        self.discard = []


class Carte(ABC):
    def __init__(self, c_id, phase):
        self.c_id = c_id
        self.phase = phase

    @abstractmethod
    def effet(self, joueur):
        ...

"""


CARTES SURVIE


"""

class Detecteur(Carte):
    """
    Evite les effets du jeton Artémia
    """
    def __init__(self, c_id, phase):
        super().__init__(self, c_id, phase)
        self.phase = 3
    def effet(self, joueur):
        if joueur.jeu.board[joueur.pos][2] == 2:
            joueur.esquive = 1
            joueur.useCard -= 1
        else:
            print("Votre lieu n'est pas ciblé par le jeton artémia, cette carte ne peut être jouée")


class Esquive(Carte):
    """
    Esquive les effets du jeton créature
    """
    def __init__(self, c_id, phase):
        super().__init__(self, c_id, phase)
        self.phase = 3
    def effet(self, joueur):
        if joueur.jeu.board[joueur.pos][2] == 1:
            joueur.esquive = 1
            joueur.useCard -= 1
        else:
            print("Votre lieu n'est pas ciblé par le jeton créature, cette carte ne peut être jouée")


class VolteFace(Carte):
    """
    Reprend en main la dernière carte Lieu jouée
    """
    def __init__(self, c_id, phase):
        super().__init__(self, c_id, phase)
        self.phase = 4
    def effet(self, joueur):
        joueur.esquive = 1
        joueur.useCard -= 1
        joueur.cartes.append(joueur.defausse[-1])
        joueur.cartes.sort()
        
class Drone(Carte):
    """
    A la place d'utiliser le pouvoir de la carte Lieu, copie le pouvoir du Rover
    """
    def __init__(self, c_id, phase):
        super().__init__(self, c_id, phase)
        self.phase = 3
    def effet(self, joueur): 
            lieuxsup = []
            for i in range(5, 10): 
                if i not in joueur.cartes and i not in joueur.defausse: 
                    lieuxsup.append(i)
            print("Vous pouvez rajouter dans votre main 1 lieu parmis ceux-ci:", lieuxsup)
            msg = f"Quel lieu voulez vous rajouter à votre main ?\n"
            cartesup = int(input(msg))
            joueur.cartes.append(cartesup)
            joueur.cartes.sort()
            
class Adrenaline(Carte): 
    """
    Récupère 1 de volonté
    """
    def __init__(self, c_id, phase):
        super().__init__(self, c_id, phase)
        self.phase = 1
    def effet(self, joueur):
        joueur.sante += 1
        
class Amplificateur(Carte):
    """
    Retire le pion Balise de la Plage pour avancer immédiatement le pion secours de 1 case 
    """
    def __init__(self, c_id, phase):
        super().__init__(self, c_id, phase)
        self.phase = 4
        def effet(self, joueur):
            #bla bla bla

class SystemeD(Carte):
    """
    Place le pion Balise sur la place
    """
    def __init__(self, c_id, phase):
        super().__init__(self, c_id, phase)
        self.phase = 1
        def effet(self, joueur):
            #bla bla bla
            
if __name__ == '__main__':
    test = Deck('survie')
    print(test.cards)
    pick = [test.draw()]
    for i in range(6):
        pick.append(test.draw())
    print(test.cards, pick)
