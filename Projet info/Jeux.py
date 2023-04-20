import Plateau
import Joueur
import Planete
import Token


class Jeux():
    def __init__(self, nbjoueurs, nomjoueurs):
        if nbjoueurs != len(nomjoueurs):
            raise ValueError
        self.board = Plateau.Plateau((2, 5, 3))
        self.players = []
        for i in range(nbjoueurs):
            self.players.append(Joueur.Joueur(i, nomjoueurs[i], self))
        self.traque = Token.Traque()
        self.secour = Token.Secour()
        self.fin = 0
        self.begin()

    def begin(self):
        val = -1
        while val != 0:
            msg = f"Etes vous prêt ?\n Oui : 0, Quitter : 1\n"
            val = int(input(msg))
            if val == 0:
                self.loop()
            elif val == 1:
                self.exit()
                return 0

    def loop(self):
        while self.fin == 0:
            self.phase1()
            self.phase2()
            self.phase3()
            self.phase4()
            self.check_victory()
            self.fin = 1

    def phase1(self):
        for player in self.players:
            player.choisir_lieu()

    def phase2(self):
        return 2

    def phase3(self):
        return 3

    def phase4(self):
        return 4

    def check_victory(self):
        if self.traque.max == self.traque.statut:
            print('Victoire de la créature')

    def exit(self):
        print("Merci d'avoir jouer !")


if __name__ == '__main__':
    test = Jeux(2,['mi','do'])

