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
    def __init__(self, c_id, phase, type):
        self.c_id = c_id
        self.type = type
        self.phase = phase

    @abstractmethod
    def effet(self, joueur):
        ...


class detecteur(Carte):
    def effet(self, joueur):
        if joueur.jeu.board[joueur.pos][2] == 2:
            joueur.esquive = 1
            joueur.useCard -= 1
        else:
            print("Votre lieu n'est pas ciblé par le jeton artémia, cette carte ne peut être jouée")


class esquive(Carte):
    """
    esquive les effets du jeton créature
    """
    def effet(self, joueur):
        if joueur.jeu.board[joueur.pos][2] == 1:
            joueur.esquive = 1
            joueur.useCard -= 1
        else:
            print("Votre lieu n'est pas ciblé par le jeton créature, cette carte ne peut être jouée")


class volteFace(Carte):
    def effet(self, joueur):
        joueur.esquive = 1


if __name__ == '__main__':
    test = Deck('survie')
    print(test.cards)
    pick = [test.draw()]
    for i in range(6):
        pick.append(test.draw())
    print(test.cards, pick)
