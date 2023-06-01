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
    Fonction représentant le paquet de cartes, la pioche en quelque sorte
    """

    def __init__(self):
        self.cards = []
        self.discard = []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            print("Il n'y a plus de cartes dans le deck, la défausse a été mélangée")
            self.reset()
        draw = self.cards.pop(0)
        return draw

    def defausser(self, card):
        self.discard.append(card)

    def reset(self):
        self.cards = self.discard.copy()
        random.shuffle(self.cards)
        self.discard = []


class DeckSurvie(Deck):
    def __init__(self):
        super().__init__()
        self.cards = [
            Detecteur(1),
            Esquive(2),
            VolteFace(3),
            Drone(4),
            Adrenaline(5),
            Amplificateur(6),
            SystemeD(7),
            Riposte(8),
            SixiemeSens(9),
            Hologramme(10),
            Portail(11),
            Fausse_Piste(12),
            Portail(13),
            Vortex(14),
            Sacrifice(15)
        ]
        self.shuffle()


class Carte(ABC):
    """
    Classe regroupant tous les types de cartes.
    Classe abstraite, il n'existe que des cartes spécifiques
    surtout utile pour l'IHM
    """

    def __init__(self, c_id, phase):
        self.c_id = c_id
        self.phase = phase

    @abstractmethod
    def effet(self, joueur):
        ...

    @abstractmethod
    def description(self):
        ...

 

'''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''





         CARTES SURVIE 





'''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''



class Detecteur(Carte):
    """
    Evite les effets du jeton Artémia
    """
    def __init__(self, c_id):
        super().__init__(c_id, 3)

    def __repr__(self):
        return "Detecteur"

    def effet(self, joueur):
        if joueur.jeu.board[joueur.pos][2] == 2:
            joueur.esquive = 1
            joueur.useCard -= 1
            joueur.survie.remove(self)
            joueur.jeu.DeckSurvie.defausser(self)
        else:
            print("Votre lieu n'est pas ciblé par le jeton artémia, cette carte ne peut être jouée")

    def description(self):
        return "Elle permet d'éviter les effets du jeton Artémia"


class Esquive(Carte):
    """
    Esquive les effets du jeton créature
    """

    def __init__(self, c_id):
        super().__init__(c_id, 3)

    def __repr__(self):
        return "Esquive"

    def effet(self, joueur):
        if joueur.jeu.board[joueur.pos][2] == 1:
            joueur.esquive = 1
            joueur.useCard -= 1
            joueur.survie.remove(self)
            joueur.jeu.DeckSurvie.defausser(self)
        else:
            print("Votre lieu n'est pas ciblé par le jeton créature, cette carte ne peut être jouée")

    def description(self):
        return "Elle permet d'éviter les effets du jeton créature"


class VolteFace(Carte):
    """
    Reprend en main la dernière carte Lieu jouée
    """

    def __init__(self, c_id):
        super().__init__(c_id, 4)

    def __repr__(self):
        return "Volte Face"

    def effet(self, joueur):
        joueur.survie.remove(self)
        joueur.jeu.DeckSurvie.defausser(self)
        joueur.useCard -= 1
        joueur.esquive = 1

    def description(self):
        return "Elle permet de reprendre en main la carte lieu jouée à ce tour"


class Drone(Carte):
    """
    A la place d'utiliser le pouvoir de la carte Lieu, copie le pouvoir du Rover
    """

    def __init__(self, c_id):
        super().__init__(c_id, 3)

    def __repr__(self):
        return "Drone"

    def effet(self, joueur):
        lieuxsup = []
        for i in range(5, 10):
            if i not in joueur.cartes and i not in joueur.defausse:
                lieuxsup.append(i)
        print("Vous pouvez rajouter dans votre main 1 lieu parmis ceux-ci:", lieuxsup)
        msg = f"Quel lieu voulez vous rajouter à votre main ?\n"
        cartesup = int(input(msg))
        joueur.cartes.append(cartesup)
        joueur.useCard -= 1
        joueur.survie.remove(self)
        joueur.jeu.DeckSurvie.defausser(self)

    def description(self):
        return "Elle permet d'utiliser le pouvoir du rover plutôt que celui du lieu actuel"


class Adrenaline(Carte):
    """
    Récupère 1 de volonté
    """

    def __init__(self, c_id):
        super().__init__(c_id, 1)

    def __repr__(self):
        return "Adrénaline"

    def effet(self, joueur):
        joueur.sante += 1
        joueur.useCard -= 1
        joueur.survie.remove(self)
        joueur.jeu.DeckSurvie.defausser(self)

    def description(self):
        return "Elle permet de récupérer 1 de volonté"


class Amplificateur(Carte):
    """
    Retire le pion Balise de la Plage pour avancer immédiatement le pion secours de 1 case
    """

    def __init__(self, c_id):
        super().__init__(c_id, 4)

    def __repr__(self):
        return "Amplificateur"

    def effet(self, joueur):
        if Plage.balise:
            joueur.survie.remove(self)
            joueur.jeu.DeckSurvie.defausser(self)
            joueur.useCard -= 1
            print("Vous retirez la balise de la plage, le jeton secours avance de 1")
            joueur.jeu.secours.avancer()
        else:
            print("Vous ne pouvez pas jouer cette carte car la balise n'est pas sur la plage")

    def description(self):
        return "Elle permet d'enlever la balise de la plage et donc d'avancer le jeton secours de 1"


class SystemeD(Carte):
    """
    Place le pion Balise sur la place
    """

    def __init__(self, c_id):
        super().__init__(c_id, 1)

    def __repr__(self):
        return "SystemeD"

    def effet(self, joueur):
        if Plage.played:
            print("Vous ne pouvez pas jouer cette carte car la balise est pas sur la plage")
        else:
            joueur.survie.remove(self)
            joueur.jeu.DeckSurvie.defausser(self)
            print("Vous placez la balise sur la plage")
            Plage.balise = True
            joueur.useCard -= 1

    def description(self):
        return "Elle permet de placer la balise sur la plage"


class Riposte(Carte):
    """
    Tire 2 cartes Traque au hasard de la main de la Créature et les place sous la pioche Traque
    """

    def __init__(self, c_id):
        super().__init__(c_id, 1)

    def __repr__(self):
        return "Riposte"

    def effet(self, joueur):
        joueur.survie.remove(self)
        joueur.jeu.DeckSurvie.defausser(self)
        joueur.useCard -= 1
        random.shuffle(joueur.jeu.creature.traque)
        c0 = joueur.jeu.creature.traque[0]
        c1 = joueur.jeu.creature.traque[1]
        joueur.jeu.creature.traque = [joueur.jeu.creature.traque[2]]
        joueur.jeu.DeckTraque.cards.append(c0)
        joueur.jeu.DeckTraque.cards.append(c1)

    def description(self):
        return "Elle permet de piocher 2 cartes traques dans la main de la créature et les mettre sous la pioche"


class SixiemeSens(Carte):
    """
    Reprend en main 2 cartes Lieu de la défausse
    """

    def __init__(self, c_id):
        super().__init__(c_id, 1)

    def __repr__(self):
        return "Sixième Sens"

    def effet(self, joueur):
        joueur.survie.remove(self)
        joueur.jeu.DeckSurvie.defausser(self)
        joueur.useCard -= 1
        joueur.reprendreDefausse()
        joueur.reprendreDefausse()

    def description(self):
        return "Elle permet de reprendre en main 2 cartes présente dans votre défausse"


class Hologramme(Carte):
    """
    Déplacez le jeton Artémia sur un lieu adjacent
    """

    def __init__(self, c_id):
        super().__init__(c_id, 3)

    def __repr__(self):
        return "Hologramme"

    def effet(self, joueur):
        if len(joueur.jeu.creature.jetons) > 2 and joueur.jeu.creature.jetons[1] == 2:
            joueur.survie.remove(self)
            joueur.jeu.DeckSurvie.defausser(self)
            voisins = joueur.jeu.board.voisin(joueur.jeu.creature.artemia)
            print("Vous pouvez déplacer le jeton Artémia sur un de ces lieux:", voisins)
            msg = f"Sur quel lieu voulez-vous le mettre ?\n"
            joueur.jeu.creature.artemia = int(input(msg))
            joueur.useCard -= 1
            joueur.esquive = 1
        else:
            print("Le jeton Artémia n'est pas sur le plateau, vous ne pouvez pas jouer cette carte")

    def description(self):
        return "Elle permet de déplacer le jeton Artémia sur un lieu adjacent"


class Portail(Carte):
    def __init__(self, c_id):
        super().__init__(c_id, 3)

    def __repr__(self):
        return "Portail"

    def effet(self, joueur):
        joueur.survie.remove(self)
        joueur.jeu.DeckSurvie.defausser(self)
        joueur.useCard -= 1
        voisins = joueur.jeu.board.voisin(joueur.pos)
        voisins_libre = []
        for voisin in voisins:
            if joueur.jeu.board[voisin][2] == 0:
                voisins_libre.append(voisin)
        print("Lieux adjacents dont le pouvoir peut être copié: ", voisins_libre)
        msg = f"Quel lieu voulez-vous copier?\n"
        lieu = int(input(msg))
        joueur.jeu.board.activer_lieu(joueur.jeu.board, joueur, lieu)

    def description(self):
        return "Elle permet de copier le pouvoir d'un lieu adjacent"


class Fausse_Piste(Carte):
    def __init__(self, c_id):
        super().__init__(c_id, 3)

    def __repr__(self):
        return "Fausse Piste "

    def effet(self, joueur):
        joueur.survie.remove(self)
        joueur.jeu.DeckSurvie.defausser(self)
        voisins = joueur.jeu.board.voisin(joueur.jeu.creature.pos)
        print("Vous pouvez déplacer le jeton Créature sur un de ces lieux:", voisins)
        msg = f"Sur quel lieu voulez-vous le mettre ?\n"
        joueur.jeu.creature.pos = int(input(msg))
        joueur.useCard -= 1
        joueur.esquive = 1

    def description(self):
        return "Elle permet de déplacer le jeton Créature sur un lieu adjacent"


class Vortex(Carte):
    def __init__(self, c_id):
        super().__init__(c_id, 2)

    def __repr__(self):
        return "Vortex"

    def effet(self, joueur):
        if len(joueur.defausse) <= 0:
            print('Votre défausse est vide, vous ne pouvez pas utiliser cette carte')
        else:
            joueur.survie.remove(self)
            joueur.jeu.DeckSurvie.defausser(self)
            joueur.useCard -= 1
            print("Vos lieux défaussés sont : ", joueur.defausse)
            msg = f"Quelle carte voulez vous jouer?\n"
            val = int(input(msg))
            joueur.defausseCarte(joueur, 0)
            joueur.pos = val

    def description(self):
        return "Elle permet d'échanger la carte Lieu jouée contre une carte Lieu de la défausse "


class Sacrifice(Carte):

    def __init__(self, c_id):
        super().__init__(c_id, 1)

    def __repr__(self):
        return "Sacrifice"

    def effet(self, joueur):
        joueur.defausseCarte(1)
        joueur.jeu.creature.useCard = 0
        joueur.survie.remove(self)
        joueur.jeu.DeckSurvie.defausser(self)
        joueur.useCard -= 1

    def description(self):
        return "Elle permet si vous défaussez une carte lieu d'empêcher la créature de jouer une carte traque"
    
 

'''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''





         CARTES TRAQUE 





'''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''

    
    
class Virus(Carte): 
    
    def __init__(self, c_id):
        super().__init__(c_id, 2)
          
    def __repr__(self):
        return "Virus"
    
    def effet(self, creature): 
        msg = f"Placer le jeton Artémia : >>\n"
        creature.artemia = int(input(msg))
        
    
 class Hurlements(Carte):
    
     def __init__(self, c_id):
        super().__init__(c_id, 2)
        
     
    def __repr__(self):
        return "Hurlements"
    
     def effet(self, joueur): 
        
        
        
class Desespoir(Carte):
    
    def __init__(self, c_id):
        super().__init__(c_id, 1)
    
    def __repr__(self):
        return "Désespoir"
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
class Lieu():
    """
    Classe regroupant tous les lieux
    """

    @abstractmethod
    def effet(self, joueur):
        ...

    @abstractmethod
    def car(self):
        ...

    def __str__(self):
        return self.car()

    def __repr__(self):
        return self.car()


class Antre(Lieu):
    def effet(self, joueur):
        val = -1
        while val != 0:
            print(f"La créature est sur le lieu {joueur.jeu.creature.pos}")
            msg = f"Voulez-vous reprendre en main votre défausse ou copier le pouvoir du jeton Créature ?\n défausse : 0, copie : 1\n >> "
            val = int(input(msg))
            if val == 0:
                joueur.reprendre_toute_defausse()
            elif val == 1:
                joueur.jeu.board.activer_lieu(joueur, joueur.jeu.creature.pos)
                val = 0

    def car(self):
        return 'Antre'


class Jungle(Lieu):
    def effet(self, joueur):
        print(f"Vous pouvez reprendre en main cette carte (la jungle) et une carte lieu de votre défausse")
        joueur.esquive = 1
        joueur.reprendreDefausse()

    def car(self):
        return 'Jungle'


class Riviere(Lieu):
    def effet(self, joueur):
        print(f"Au prochain tour vous choisirai deux lieux et révélerai celui de votre choix en phase 3")
        joueur.River = True

    def car(self):
        return 'Riviere'


class Plage(Lieu):
    balise = False
    played = False

    def effet(self, joueur):
        if Plage.played:
            print(
                "La plage a déjà été jouée à ce tour, vous ne pouvez donc pas activer la balise\n A la place vous reprenez en main une carte de votre défausse")
            joueur.reprendreDefausse()
        elif Plage.balise:
            print("Vous retirez la balise de la plage, le jeton secours avance de 1")
            joueur.jeu.secours.avancer()
            Plage.played = True
        else:
            print("Vous placez la balise sur la plage")
            Plage.balise = True
            Plage.played = True

    def car(self):
        return 'Plage'


class Rover(Lieu):
    def effet(self, joueur):
        lieuxsup = []
        for i in range(5, 10):
            if i not in joueur.cartes and i not in joueur.defausse:
                lieuxsup.append(i)
        if len(lieuxsup) == 0:
            print("Vous avez déjà tous les lieux, vous pouvez donc reprendre une carte en main à la place de jouer le rover")
            joueur.reprendreDefausse()
            return 1
        print("Vous pouvez rajouter dans votre main 1 lieu parmis ceux-ci:", lieuxsup)
        msg = f"Quel lieu voulez vous rajouter à votre main ?\n"
        cartesup = int(input(msg))
        joueur.cartes.append(cartesup)

    def car(self):
        return 'Rover'


class Marais(Lieu):
    def effet(self, joueur):
        print(f"Vous pouvez reprendre en main cette carte (le marais) et deux cartes lieux de votre défausse")
        joueur.esquive = 1
        joueur.reprendreDefausse()
        joueur.reprendreDefausse()

    def car(self):
        return 'Marais'


class Abri(Lieu):
    def effet(self, joueur):
        carte1 = joueur.jeu.DeckSurvie.draw()
        carte2 = joueur.jeu.DeckSurvie.draw()
        print(f"Voici la première carte {carte1}?\n{carte1.description()}")
        print(f"Voici la deuxième carte {carte2}?\n{carte2.description()}")
        msg = "Quel carte voulez vous choisir ?\n pour la première carte entrez : 1\npour la deuxième carte entrez: 2\n>> "
        val = int(input(msg))
        if val == 1:
            joueur.survie.append(carte1)
        else:
            joueur.survie.append(carte2)

    def car(self):
        return 'Abri'


class Epave(Lieu):
    played = False

    def effet(self, joueur):
        if Epave.played:
            print("L'épave a déjà été jouée à ce tour, vous ne pouvez donc pas activer la balise\n A la place vous reprenez en main une carte de votre défausse")
            joueur.reprendreDefausse()
        else:
            print("Le jeton secours avance de 1")
            joueur.jeu.secours.avancer()
            Epave.played = True

    def car(self):
        return 'Epave'


class Source(Lieu):
    def effet(self, joueur):
        msg = "Voulez-vous piocher une carte survie ou rendre 1 de volonté à un joueur ?\nPiocher une carte : 1, Rendre un point de volonté : 2\n>> "
        val = int(input(msg))
        if val == 2:
            for player in joueur.jeu.players:
                if player.sante < 3:
                    print(player)
                    print(f"Santé de {player.sante}")
                    msg = "Voulez-vous rendre de la volonté à ce joueur ?\nOui : 0, Non :1\n>> "
                    val = int(input(msg))
                    if val == 0:
                        player.sante += 1
                        return 1
            print("Vous n'avez pas rendu de volonté à un joueur, vous piochez donc une carte survie à la place")
        else:
            joueur.pick()

    def car(self):
        return 'Source'


class Artefact(Lieu):
    def effet(self, joueur):
        print(f"Au prochain tour vous choisirai deux lieux et révélerai celui de votre choix en phase 3")
        joueur.Artefact = True

    def car(self):
        return 'Artefact'


if __name__ == '__main__':
    print('yo')
