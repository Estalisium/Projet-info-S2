import unittest
import math
import Joueur
import Jeux


class TestJoueur(unittest.TestCase):
    """
    Test de la classe Joueur
    """
    def test_init(self):
        """
        Test de l'initialisation
        """
        jeu = Jeux.Jeux(2, ['Marie', 'Alix'], [1, 'Alix'])
        Marie = Joueur.Joueur(1, 'Marie', jeu)
        self.assertEqual(Marie.jeu, jeu)
        self.assertEqual(Marie.nom, 'Marie')
        self.assertEqual(len(Marie.survie), 1)
        self.assertEqual(len(Marie.cartes), 5)

    def test_defausseCarte(self):
        """
        Test de la fonction defausseCarte, en mode 0 (c'est-à-dire celle utilisée en phase 4)
        """
        jeu = Jeux.Jeux(2, ['Marie', 'Alix'], [1, 'Alix'])
        Marie = Joueur.Joueur(1, 'Marie', jeu)
        Marie.pos = 2
        Marie.defausseCarte(0)
        self.assertEqual(Marie.defausse, [2])
        self.assertFalse(2 not in Marie.cartes)
        Marie.esquive = 1
        Marie.pos = 2
        Marie.defausseCarte(0)
        self.assertEqual(Marie.defausse, [])
        self.assertFalse(2 in Marie.cartes)

    def test_lacher_prise(self):
        """
        Test de la fonction lacher prise
        """
        jeu = Jeux.Jeux(2, ['Marie', 'Alix'], [1, 'Alix'])
        Marie = Joueur.Joueur(1, 'Marie', jeu)
        Marie.sante = 1
        Marie.pos = 2
        Marie.defausseCarte(0)
        Marie.lacher_prise()
        self.assertEqual(Marie.sante, 3)
        self.assertEqual(Marie.jeu.traque.statut, 1)
        self.assertEqual(Marie.defausse, [])

    def test_creature(self):
        """
        Test de la fonction creature
        """
        jeu = Jeux.Jeux(2, ['Marie', 'Alix'], [1, 'Alix'])
        Marie = Joueur.Joueur(1, 'Marie', jeu)
        Marie.pos = 0
        Marie.creature()
        self.assertEqual(Marie.sante, 1)
        self.assertEqual(Marie.jeu.creature.eat, 1)
        self.assertEqual(Marie.jeu.traque.statut, 1)
        Marie.pos = 1
        Marie.creature()
        self.assertEqual(Marie.sante, 3)


if __name__ == '__main__':
    unittest.main()