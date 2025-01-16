import unittest
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hypergeom  # Para el cálculo de la distribución teórica
from Jeu.Bateau import Bateau
from Jeu.Bataille import Bataille

class TestSimulationAleatoire(unittest.TestCase):

    def setUp(self):
        """
        Initialiser la bataille et les bateaux avant chaque test.
        """
        grille_size = 10
        # Créer les bateaux avec des longueurs différentes
        self.liste_bateaux = [Bateau(1), Bateau(2), Bateau(3), Bateau(4), Bateau(5)]
        # Initialiser l'objet Bataille avec une grille de taille 10x10 et les bateaux
        self.bataille = Bataille(grille_size, grille_size, self.liste_bateaux)

    def test_esperance_theorique(self):
        """
        Vérifie que l'espérance théorique est calculée correctement.
        """
        resultats = self.bataille.joue("aleatoire")
        esperance_theorique = np.mean(resultats)
        print("Esperance théorique aléatoire : ", esperance_theorique)

        # L'espérance doit être un nombre positif
        self.assertGreater(esperance_theorique, 0, "L'espérance théorique doit être un nombre positif.")

    def test_distribution_theorique(self):
        """
        Vérifie que la distribution théorique est calculée correctement.
        """
        N = 100  # Nombre total de cases dans la grille
        m = 17  # Nombre de cases occupées par les bateaux
        k_max = 100  # Nombre maximum de coups

        # Calculer la distribution hypergéométrique pour chaque nombre de tirs
        distrib_theorique = [hypergeom.pmf(17, N, m, k) for k in range(17, k_max + 1)]

        # Normalisation de la distribution pour que la somme soit égale à 1
        distrib_theorique = [p / sum(distrib_theorique) for p in distrib_theorique]

        # Vérification que la somme des probabilités théoriques est correcte
        self.assertAlmostEqual(sum(distrib_theorique), 1, delta=0.01,
                               msg="La somme des probabilités de la distribution théorique doit être proche de 1.")

        # Tracé de la distribution théorique
        plt.figure(figsize=(10, 6))
        plt.bar(range(17, k_max + 1), distrib_theorique, color='orange', alpha=0.6, label='Distribution théorique')
        plt.title("Distribution du nombre de coups aléatoirement")
        plt.xlabel("Nombre de coups")
        plt.ylabel("Probabilité")
        plt.legend()
        plt.show()

    def test_simuler_aleatoire(self):
        """
        Vérifie que la simulation aléatoire retourne des résultats cohérents.
        """
        # Simuler 1000 parties aléatoires
        resultats = self.bataille.joue("aleatoire")

        # Vérifier que la liste des résultats contient 1000 entrées
        self.assertEqual(len(resultats), 1000, "La simulation doit retourner 1000 résultats.")

        # Vérifier que chaque résultat est un nombre entier positif (le nombre de coups)
        for res in resultats:
            self.assertTrue(isinstance(res, int), "Le nombre de coups doit être un entier.")
            self.assertGreater(res, 0, "Le nombre de coups doit être supérieur à 0.")

    def test_donnees_histogramme(self):
        """
        Vérifie que les données pour l'histogramme sont générées correctement et affiche un histogramme amélioré.
        """
        resultats = self.bataille.joue("aleatoire")

        # Calcul de statistiques
        esperance = np.mean(resultats)
        std_dev = np.std(resultats)

        # Créer un histogramme avec des améliorations visuelles, en affichant la distribution de probabilité
        plt.figure(figsize=(10, 6))
        plt.hist(resultats, bins=range(min(resultats), max(resultats) + 1), edgecolor='black', color='skyblue',
                 density=True)
        plt.title(f"Distribution du nombre de coups aléatoirement\n"
                  f"Espérance: {esperance:.2f}, Écart-type: {std_dev:.2f}", fontsize=14)
        plt.xlabel("Nombre de coups", fontsize=12)
        plt.ylabel("Probabilité", fontsize=12)  # Changer 'Fréquence' à 'Probabilité'
        plt.axvline(esperance, color='red', linestyle='dashed', linewidth=2,
                    label=f"Espérance: {esperance:.2f}")
        plt.legend()

        # Afficher l'histogramme
        plt.show()

        # Vérifier que les résultats sont cohérents
        self.assertTrue(min(resultats) < max(resultats), "Les résultats doivent contenir une plage valide de valeurs.")

    def test_comparaison_theorique_empirique(self):
        """
        Vérifie que la distribution théorique et l'espérance sont calculées correctement et affiche le graphique.
        """
        # Paramètres pour la distribution théorique
        N = 100  # Nombre total de cases dans la grille
        m = 17  # Nombre de cases occupées par les bateaux
        k_max = 100  # Nombre maximum de coups

        # 1. Calculer la distribution hypergéométrique pour chaque nombre de tirs
        distrib_theorique = [hypergeom.pmf(17, N, m, k) for k in range(17, k_max + 1)]

        # Normalisation de la distribution pour que la somme soit égale à 1
        distrib_theorique = [p / sum(distrib_theorique) for p in distrib_theorique]

        # Vérification que la somme des probabilités théoriques est correcte
        self.assertAlmostEqual(sum(distrib_theorique), 1, delta=0.01,
                               msg="La somme des probabilités de la distribution théorique doit être proche de 1.")

        # 2. Simulation des résultats empiriques
        resultats_aleatoires = self.bataille.joue("aleatoire")

        # Calcul de l'espérance empirique
        esperance_empirique = np.mean(resultats_aleatoires)
        std_dev_empirique = np.std(resultats_aleatoires)

        # 3. Tracé des distributions théoriques et empiriques avec l'espérance
        plt.figure(figsize=(10, 6))

        # Histogramme des résultats empiriques
        bins = range(17, k_max + 1)  # Les mêmes bins que pour la distribution théorique
        bar_width = 0.4  # Largeur des barres pour éviter l'overlap

        # Décaler les barres de l'histogramme vers la gauche
        plt.hist(resultats_aleatoires, bins=bins, edgecolor='black', color='skyblue', alpha=0.6,
                 density=True, label='Résultats empiriques', align='left', rwidth=bar_width)

        # Décaler les barres de la distribution théorique vers la droite
        plt.bar(np.array(bins) + bar_width, distrib_theorique, color='orange', alpha=0.6,
                edgecolor='black', width=bar_width, label='Distribution théorique')

        # Ajout de la ligne de l'espérance empirique
        plt.axvline(esperance_empirique, color='red', linestyle='dashed', linewidth=2,
                    label=f"Espérance empirique: {esperance_empirique:.2f}")

        # Ajustements visuels
        plt.title(f"Comparaison des résultats empiriques et théoriques\n"
                  f"Espérance empirique: {esperance_empirique:.2f}, Écart-type: {std_dev_empirique:.2f}",
                  fontsize=14)
        plt.xlabel("Nombre de coups", fontsize=12)
        plt.ylabel("Probabilité / Fréquence", fontsize=12)
        plt.legend(loc='upper left')  # Déplacer la légende en haut à gauche
        plt.grid(True)  # Ajouter une grille pour plus de clarté
        plt.show()

        # Vérification de la validité des résultats
        self.assertGreater(esperance_empirique, 0, "L'espérance empirique doit être un nombre positif.")

    def tearDown(self):
        """
        Nettoyage après chaque test, si nécessaire.
        """
        pass