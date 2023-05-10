import Plateau
import Joueur
import Planete
import Token


class Jeux():
    """
    Classe principale contenant tout le déroulement de la partie
    """

    def __init__(self, nbjoueurs, nomjoueurs):
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
        self.players = []
        for i in range(nbjoueurs):
            if i != self.creature.id:
                self.players.append(Joueur.Joueur(i, nomjoueurs[i], self))
        self.traque = Token.TraqueToken()
        self.secours = Token.SecoursToken()
        self.fin = 0
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
            self.creature.eat = 0
            self.creature.useCard = 1
            for joueur in self.players:
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
        print(self.players)
        for player in self.players:
            player.choisir_lieu()

    def phase2(self):
        """
        Placement des jetons pour la créature
        """
        self.creature.placer_jetons()

    def phase3(self):
        """
        Résolution des lieux joueur par joueur
        """
        for player in self.players:
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
            player.defausseCarte(0)
        self.secours.avancer()
        self.board.reset()

    def check_victory(self):
        print(self.traque.statut)
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
