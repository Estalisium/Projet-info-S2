import Plateau
import Joueur
import Planete
import Token
import sqlite3

class Jeux():
    """
    Classe principale contenant tout le déroulement de la partie
    """

    def __init__(self, nbjoueurs, nomjoueurs, creature=None):
        """
        :param nbjoueurs: int, compris entre 2 et 7
        :param nomjoueurs: [str], doit être de la même longueur que nbjoueur contient les noms des Joueurs
        creature : objet Creature, représente la créature
        players : liste d'objets Joueur, représente la liste des joueurs
        board : objet Plateau, représente le plateau
        traque : objet TraqueToken, représente le jeton Traque
        secours : objet SecoursToken, représente le jeton Secours
        fin : 0 ou 1, 0 si aucune condition de victoire n'est atteinte, 1 si au moins une l'est
        """
        if nbjoueurs > 7 or nbjoueurs < 2 or nbjoueurs != len(nomjoueurs):
            raise ValueError
        if creature:  # Permet de réaliser les tests plus facilement
            self.creature = Joueur.Creature(creature[0], creature[1], self)
        else:
            crea = 0  # Permet de continuer la requête tant qu'une créature n'est pas choisie
            while crea == 0:
                msg = f"Qui sera la créature ?\n >> "
                val = str(input(msg))
                if val not in nomjoueurs:
                    print("Cette personne n'est pas dans la partie")
                for i in range(nbjoueurs):
                    if nomjoueurs[i] == val:
                        self.creature = Joueur.Creature(i, nomjoueurs[i], self)
                        crea = 1
        self.board = Plateau.Plateau()
        self.DeckSurvie = Planete.DeckSurvie()
        self.DeckTraque = Planete.DeckTraque()
        self.players = []
        self.IHM = False
        k = 0
        for i in range(nbjoueurs):
            if i != self.creature.id:
                self.players.append(Joueur.Joueur(i, nomjoueurs[i], self))
                self.players[k].pick()
                k += 1
        con = sqlite3.connect('Conditions_de_victoire.db')
        cur = con.cursor()
        query = "SELECT max_traque, max_secours FROM Conditions_de_victoire WHERE nombre_j = ?"
        cur.execute(query, (nbjoueurs,)) #Permet d'obtenir les conditions de victoires grâce à celles préalablement rentrées dans la base de donnée générée par Database.py
        maxs = cur.fetchone()
        self.traque = Token.TraqueToken(maxs[0])
        self.secours = Token.SecoursToken(maxs[1])
        self.fin = 0
        if not creature:  # En mettant ce test la partie ne commence pas lorsqu'on veut juste effectuer un test
            self.begin()

    def begin(self):
        """
        Initialise la partie
        """
        val = -1
        while val != 0:
            msg = f"Etes vous prêt ?\n Oui : 0, Quitter : 1\n >> "
            val = int(input(msg))
            if val == 0:
                self.loop()
            elif val == 1:
                self.exit()
                return 0

    def loop(self):
        """
        Boucle principale du jeu, continue jusqu'à ce qu'une condition de victoire soit atteinte (fin = 1)
        """
        while self.fin == 0:
            self.board[3][3].played = False  # reset de la Plage
            self.board[7][3].played = False  # reset de l'Epave
            self.creature.eat = 0
            self.creature.useCard = 1
            for joueur in self.players:
                joueur.cartes.sort()
                joueur.useCard = 1
            self.phase1()
            self.phase2()
            self.phase3()
            self.phase4()
            self.check_victory()

    def phase1(self):
        """
        Choix du lieu pour chaque joueur
        """
        for player in self.players:
            print(player)
            player.jouerCarte(1)
            player.choisir_lieu()

    def phase2(self):
        """
        Placement des jetons pour la créature
        """
        for player in self.players:
            player.jouerCarte(2)
        self.creature.placer_jetons()

    def phase3(self):
        """
        Résolution des lieux joueur par joueur
        """
        print(f"Le jeton Créature se situe sur le lieu {self.creature.pos}")
        if len(self.creature.jetons) > 1:
            if self.creature.jetons[1] == 2:
                print(f"Le jeton Artemia se situe sur le lieu {self.creature.artemia}")
        for player in self.players:
            player.jouerCarte(3)
            if player.River:
                print(f"Vous avez jouez ces deux lieux : {player.pos}, {player.posRiver}")
                msg = f"Lequel voulez vous activer?\n >> "
                val = int(input(msg))
                if val != player.pos:
                    player.pos = player.posRiver
                player.River = False
            if player.Artefact:
                print(f"Vous avez jouez ces deux lieux : {player.pos}, {player.posRiver}")
                crea = player.jeu.board[player.posRiver][2]
                if crea == 0:
                    self.board.activer_lieu(player, player.posRiver)
                elif crea == 1:
                    player.creature()
                elif crea == 2:
                    player.artemia()
            crea = player.jeu.board[player.pos][2]
            if crea == 0:
                self.board.activer_lieu(player, player.pos)
            elif crea == 1:
                player.creature()
            elif crea == 2:
                player.artemia()

    def phase4(self):
        """
        La créature reprend ses jetons, les joueurs défaussent leur(s) lieu(x) joué(s) et le jeton secours avance de 1
        """
        for player in self.players:
            player.jouerCarte(4)
            player.defausseCarte(0)
        self.secours.avancer()
        self.board.reset()
        print("Fin du tour")

    def check_victory(self):
        print(f"Le jeton traque est à {self.traque.statut}/{self.traque.max} et le jeton secours à {self.secours.statut}/{self.secours.max}")
        if self.secours.statut%2 == 1:
            self.creature.jetons.append(2)
        else:
            self.creature.jetons = [1]
        if self.traque.max == self.traque.statut:
            print(self.traque.statut)
            print('Victoire de la créature')
            self.fin = 1
            self.exit()
        elif self.secours.max == self.secours.statut:
            print('Victoire des Chassés')
            self.fin = 1
            self.exit()

    def exit(self):
        print("Merci d'avoir jouer, à bientôt !")


if __name__ == "__main__":
    print('------------------------------------------------')
    print('|   Bienvenue sur le jeu Not Alone !   |')
    print("------------------------------------------------\n")
    nb_joueurs = int(input("A combien  voulez-vous jouer ?\n >> "))
    names = []
    for i in range(nb_joueurs):
        names.append(input(f"Comment s'appelle le joueur {i} ?\n >> "))
    Jeux(nb_joueurs, names)
