import unittest
import numpy as np
import matplotlib.pyplot as plt
from Jeu.Bataille import Bataille
from Jeu.Bateau import Bateau
from Jeu.Joueur import Joueur

class TestSimulationHeuristique(unittest.TestCase):

    def setUp(self):
        """
        Initialiser la bataille et les bateaux avant chaque test.
        """
        grille_size = 10
        # Créer les bateaux avec des longueurs différentes
        self.liste_bateaux = [Bateau(1), Bateau(2), Bateau(3), Bateau(4), Bateau(5)]
        # Initialiser l'objet Bataille avec une grille de taille 10x10 et les bateaux
        self.bataille = Bataille(grille_size, grille_size, self.liste_bateaux)
        # Créer un joueur associé à cette bataille
        self.joueur = Joueur(self.bataille)

    def test_simuler_heuristique(self):
        """
        Vérifie que la simulation heuristique retourne des résultats cohérents.
        """
        # Simuler 1000 parties heuristiques
        resultats = [self.joueur.jouee_heuristique() for _ in range(1000)]

        # Vérifier que la liste des résultats contient 1000 entrées
        self.assertEqual(len(resultats), 1000, "La simulation doit retourner 1000 résultats.")

        # Vérifier que chaque résultat est un nombre entier positif (le nombre de coups)
        for res in resultats:
            self.assertTrue(isinstance(res, int), "Le nombre de coups doit être un entier.")
            self.assertGreater(res, 0, "Le nombre de coups doit être supérieur à 0.")

    def test_esperance_theorique(self):
        """
        Vérifie que l'espérance théorique est calculée correctement pour la stratégie heuristique.
        """
        resultats = [self.joueur.jouee_heuristique() for _ in range(1000)]
        esperance_theorique = np.mean(resultats)
        print("Espérance théorique (Heuristique) : ", esperance_theorique)

        # L'espérance doit être un nombre positif
        self.assertGreater(esperance_theorique, 0, "L'espérance théorique doit être un nombre positif.")

    def test_donnees_histogramme(self):
        """
        Vérifie que les données pour l'histogramme sont générées correctement et affiche un histogramme amélioré.
        """
        resultats = [self.joueur.jouee_heuristique() for _ in range(1000)]

        # Calcul de statistiques
        esperance_theorique = np.mean(resultats)
        std_dev = np.std(resultats)

        # Créer un histogramme avec des améliorations visuelles (distribution de probabilité)
        plt.figure(figsize=(10, 6))
        plt.hist(resultats, bins=range(min(resultats), max(resultats) + 1), edgecolor='black', color='green',
                 density=True)
        plt.title(f"Distribution du nombre de coups (Stratégie heuristique)\n"
                  f"Espérance théorique: {esperance_theorique:.2f}, Écart-type: {std_dev:.2f}", fontsize=14)
        plt.xlabel("Nombre de coups", fontsize=12)
        plt.ylabel("Probabilité", fontsize=12)  # Modifier l'étiquette pour indiquer la probabilité
        plt.axvline(esperance_theorique, color='red', linestyle='dashed', linewidth=2,
                    label=f"Espérance: {esperance_theorique:.2f}")
        plt.legend()

        # Afficher l'histogramme
        plt.show()

        # Vérifier que les résultats sont cohérents
        self.assertTrue(min(resultats) < max(resultats), "Les résultats doivent contenir une plage valide de valeurs.")

    def test_comparaison_aleatoire_heuristique(self):
        """
        Compare les distributions de probabilité entre la stratégie aléatoire et la stratégie heuristique.
        """
        # 1. Résultats de la stratégie heuristique
        resultats_heuristique = [self.joueur.jouee_heuristique() for _ in range(1000)]
        esperance_heuristique = np.mean(resultats_heuristique)
        std_dev_heuristique = np.std(resultats_heuristique)

        # 2. Résultats de la stratégie aléatoire
        resultats_aleatoire = self.bataille.joue("aleatoire")
        esperance_aleatoire = np.mean(resultats_aleatoire)
        std_dev_aleatoire = np.std(resultats_aleatoire)

        # 3. Création de l'histogramme comparatif
        plt.figure(figsize=(10, 6))

        # Histogramme pour la stratégie heuristique (en vert)
        plt.hist(resultats_heuristique, bins=range(min(resultats_heuristique), max(resultats_heuristique) + 1),
                 edgecolor='black', color='green', alpha=0.6, density=True, label='Stratégie heuristique')

        # Histogramme pour la stratégie aléatoire (en bleu)
        plt.hist(resultats_aleatoire, bins=range(min(resultats_aleatoire), max(resultats_aleatoire) + 1),
                 edgecolor='black', color='skyblue', alpha=0.6, density=True, label='Stratégie aléatoire')

        # Ajout des lignes de l'espérance
        plt.axvline(esperance_heuristique, color='red', linestyle='dashed', linewidth=2,
                    label=f"Espérance heuristique: {esperance_heuristique:.2f}")
        plt.axvline(esperance_aleatoire, color='orange', linestyle='dashed', linewidth=2,
                    label=f"Espérance aléatoire: {esperance_aleatoire:.2f}")

        # 4. Ajustements visuels
        plt.title(f"Comparaison des stratégies heuristique et aléatoire\n"
                  f"Espérance heuristique: {esperance_heuristique:.2f}, Écart-type: {std_dev_heuristique:.2f}\n"
                  f"Espérance aléatoire: {esperance_aleatoire:.2f}, Écart-type: {std_dev_aleatoire:.2f}",
                  fontsize=14)
        plt.xlabel("Nombre de coups", fontsize=12)
        plt.ylabel("Probabilité", fontsize=12)
        plt.legend(loc='upper left')
        plt.grid(True)

        # 5. Afficher l'histogramme
        plt.show()

        # Vérification de la validité des résultats
        self.assertTrue(min(resultats_aleatoire) < max(resultats_aleatoire),
                        "Les résultats aléatoires doivent contenir une plage valide de valeurs.")
        self.assertTrue(min(resultats_heuristique) < max(resultats_heuristique),
                        "Les résultats heuristiques doivent contenir une plage valide de valeurs.")


    def tearDown(self):
        """
        Nettoyage après chaque test, si nécessaire.
        """
        pass

