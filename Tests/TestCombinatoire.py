import unittest

from Jeu.Bateau import Bateau
from Jeu.GrilleMathematique import GrilleMathematique

class TestCombinatoire(unittest.TestCase):
    def setUp(self):
        # Configuración inicial común para los tests
        self.grille = GrilleMathematique(10, 10)  # Grille de 10x10
        self.bateau1 = Bateau(1)  # Bateau de longueur 5
        self.bateau2 = Bateau(2)  # Bateau de longueur 4
        #self.bateau3 = Bateau(3)  # Bateau de longueur 3
        #self.bateau4 = Bateau(4)  # Bateau de longueur 3
        #self.bateau5 = Bateau(5)  # Bateau de longueur 2
        self.liste_bateaux = [self.bateau1, self.bateau2]

    def test_nb_bateau(self):
        # Test pour la méthode nb_bateau
        result = self.bateau1.nb_bateau(self.grille)
        print("Le nombre de positions possibles pour un bateau de longueur 5 est ", result)
        self.assertTrue(result > 0, "Le nombre de positions possibles devrait être supérieur à 0.")

        result = self.bateau2.nb_bateau(self.grille)
        print("Le nombre de positions possibles pour un bateau de longueur 4 est ", result)
        self.assertTrue(result > 0, "Le nombre de positions possibles devrait être supérieure à 0.")
        return 0

    def test_nb_liste_bateaux(self):
        # Test pour la méthode nb_liste_bateaux
        result = self.grille.nb_liste_bateaux(self.liste_bateaux)
        print("nb_liste_bateaux -> Nombre de configurations possibles avec 3 bateaux : ", result)
        self.assertTrue(result > 0, "Le nombre de configurations possibles devrait être supérieur à 0.")

    def test_prob_grille(self):
        # Test para el método prob_grille
        for i in range(5) :
            self.grille.genere_grille(self.liste_bateaux)
            result = self.grille.prob_grille(self.liste_bateaux, timeout=10)
            print("Tentatives pour trouver une grille donnée : ", result)
            self.assertTrue(result == -1 or result > 0,
                        "Le nombre de tentatives devrait être soit un timeout, soit supérieur à 0.")

    def test_nb1_liste_bateaux(self):
        # Test para el método approx_nb_liste_bateaux
        result = self.grille.nb1_liste_bateaux(self.liste_bateaux)
        print("nb1_liste_bateaux -> Nombre de configurations possibles aproximées avec 3 bateaux : ", result)
        self.assertTrue(result > 0, "L'approximation du nombre de configurations devrait être supérieure à 0.")

    def test_nb2_liste_bateaux(self):
        # Test para el método approx_nbGrille2
        result = self.grille.nb2_liste_bateaux(self.liste_bateaux)
        print("nb2_liste_bateaux -> Nombre de configurations possibles aproximées avec 3 bateaux : ", result)
        self.assertTrue(result > 0, "Le nombre d'approximations de grilles devrait être supérieur à 0.")