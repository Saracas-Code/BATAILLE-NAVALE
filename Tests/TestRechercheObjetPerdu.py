import unittest
from Jeu.RechercheObjetPerdu import RechercheObjetPerdu
from Jeu.GrilleMathematique import GrilleMathematique

class TestRechercheObjetPerdu(unittest.TestCase):
    
    def setUp(self):
        # Initialisation d'une grille 10x10
        self.grille = GrilleMathematique(10, 10)  # Exemple de grille 10x10 gérée par la classe GrilleMathematique
        
        # Probabilités initiales uniformes (1 / nombre de cases)
        self.pi = [1 / (self.grille.x * self.grille.y)] * (self.grille.x * self.grille.y)
        
        # Probabilité de détection
        self.ps = 0.8  # Probabilité de détection du senseur
        
        # Positionner l'objet de manière aléatoire dans la grille
        position_x, position_y = self.grille.positionner_objet()  # Utiliser la méthode pour positionner l'objet
        self.position_objet = (position_x * self.grille.y) + position_y  # Convertir la position en index linéaire
        
        # Créer un objet RechercheObjetPerdu
        self.recherche = RechercheObjetPerdu(self.grille, self.pi, self.ps, self.position_objet)

    def test_recherche_objet(self):
        """
        Teste si l'algorithme peut trouver l'objet et renvoie un tuple (x, y) et le nombre de coups
        """
        resultat, nombre_coups = self.recherche.recherche()
        # Vérifie que le résultat est un tuple (x, y)
        self.assertTrue(isinstance(resultat, tuple), "Le résultat doit être un tuple (x, y).")
        self.assertEqual(len(resultat), 2, "Le résultat doit contenir deux éléments (x et y).")
        self.assertTrue(resultat[0] in range(self.grille.x) and resultat[1] in range(self.grille.y), "Les coordonnées doivent être valides.")
        # Vérifie que le nombre de coups est un entier positif
        self.assertTrue(isinstance(nombre_coups, int) and nombre_coups > 0, "Le nombre de coups doit être un entier positif.")
