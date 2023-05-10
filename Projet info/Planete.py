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
    Esquive les effets du jeton créature
    """
    def effet(self, joueur):
        if joueur.jeu.board[joueur.pos][2] == 1:
            joueur.esquive = 1
            joueur.useCard -= 1
        else:
            print("Votre lieu n'est pas ciblé par le jeton créature, cette carte ne peut être jouée")


class volteFace(Carte):
    """
    Reprend en main la dernière carte Lieu jouée
    """
    def effet(self, joueur):
        joueur.esquive = 1
        joueur.useCard -= 1
        joueur.cartes.append(joueur.defausse[-1])
        joueur.cartes.sort()
        
class drone(Carte):
    """
    A la place d'utiliser le pouvoir de la carte Lieu, copie le pouvoir du Rover
    """
    def effet(self, joueur): 
            lieuxsup = []
            for i in range(5, 10): 
                if i not in joueur.cartes and i not in joueur.defausse: 
                    lieuxsup.append(i)
            print("Vous pouvez rajouter dans votre main 1 lieu parmis ceux-ci:", lieuxsup)
            msg = f"Quel lieu voulez vous rajouter à votre main ?\n"
            cartesup = int(input(msg))
            
            
        
            
if __name__ == '__main__':
    test = Deck('survie')
    print(test.cards)
    pick = [test.draw()]
    for i in range(6):
        pick.append(test.draw())
    print(test.cards, pick)
