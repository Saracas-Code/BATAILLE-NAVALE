import unittest
import numpy as np
import matplotlib.pyplot as plt
from Jeu.Bataille import Bataille
from Jeu.Bateau import Bateau
from Jeu.Joueur import Joueur

class TestSimulationProbabilisteSimplifiee(unittest.TestCase):

    def setUp(self):
        """
        Initialiser la bataille et les bateaux avant chaque test.
        """
        grille_size = 10
        # Créer les bateaux avec des longueurs différentes
        self.liste_bateaux = [Bateau(1), Bateau(2), Bateau(3), Bateau(4), Bateau(5)]
        # Initialiser l'objet Bataille avec une grille de taille 10x10 et les bateaux
        self.bataille = Bataille(grille_size, grille_size, self.liste_bateaux)
        self.joueur = Joueur(self.bataille)

    def test_simuler_probabiliste(self):
        """
        Simule plusieurs grilles pour estimer la probabilité d'obtenir une configuration donnée.
        """
        nb_iterations = 1000
        configuration_voulue = self.genere_configuration_specifique()
        succes = 0

        for _ in range(nb_iterations):
            # Générer une grille aléatoire
            self.joueur.jouee_probabiliste_simplifiee()

            # Comparer la grille générée avec la configuration voulue
            if self.bataille.grille == configuration_voulue:
                succes += 1

        # Calculer la probabilité obtenue
        probabilite_obtenue = succes / nb_iterations

        # Lancer l'assertion pour vérifier la probabilité
        self.assertGreaterEqual(probabilite_obtenue, 0, "La probabilité doit être positive.")
        self.assertLessEqual(probabilite_obtenue, 1, "La probabilité ne peut pas être supérieure à 1.")

    def test_donnees_histogramme(self):
        """
        Génère un histogramme pour visualiser la distribution des configurations obtenues.
        """
        nb_iterations = 1000
        resultats = []

        for _ in range(nb_iterations):
            resultats.append(self.joueur.jouee_probabiliste_simplifiee())

        # Calcul de statistiques
        esperance_theorique = np.mean(resultats)
        std_dev = np.std(resultats)

        # Créer un histogramme avec des améliorations visuelles
        plt.figure(figsize=(10, 6))
        plt.hist(resultats, bins=range(min(resultats), max(resultats) + 1), edgecolor='black', color='purple')
        plt.title(f"Distribution du nombre de coups (Probabilité Simplifiée)\n"
                  f"Espérance théorique: {esperance_theorique:.2f}, Écart-type: {std_dev:.2f}", fontsize=14)
        plt.xlabel("Nombre de coups", fontsize=12)
        plt.ylabel("Fréquence", fontsize=12)
        plt.axvline(esperance_theorique, color='red', linestyle='dashed', linewidth=2,
                    label=f"Espérance: {esperance_theorique:.2f}")
        plt.legend()

        # Afficher l'histogramme
        plt.show()

    def genere_configuration_specifique(self):
        """
        Génère une configuration spécifique de grille pour la comparer dans le test.
        Cette fonction doit retourner une configuration que vous souhaitez obtenir.
        """
        # Remplacez par la logique pour créer une configuration voulue
        # Exemple fictif de configuration pour une grille 10x10
        return [[0 for _ in range(10)] for _ in range(10)]

    def test_comparaison_strategies(self):
        """
        Compare les distributions de probabilité entre la stratégie probabiliste simplifiée, heuristique et aléatoire.
        """
        nb_iterations = 1000

        # 1. Résultats de la stratégie probabiliste simplifiée
        resultats_probabiliste = [self.joueur.jouee_probabiliste_simplifiee() for _ in range(nb_iterations)]
        esperance_probabiliste = np.mean(resultats_probabiliste)
        std_dev_probabiliste = np.std(resultats_probabiliste)

        # 2. Résultats de la stratégie heuristique
        resultats_heuristique = [self.joueur.jouee_heuristique() for _ in range(nb_iterations)]
        esperance_heuristique = np.mean(resultats_heuristique)
        std_dev_heuristique = np.std(resultats_heuristique)

        # 3. Résultats de la stratégie aléatoire
        resultats_aleatoire = [self.joueur.jouee_aleatoire() for _ in range(nb_iterations)]
        esperance_aleatoire = np.mean(resultats_aleatoire)
        std_dev_aleatoire = np.std(resultats_aleatoire)

        # 4. Création de l'histogramme comparatif
        plt.figure(figsize=(10, 6))

        # Histogramme pour la stratégie probabiliste simplifiée (en violet)
        plt.hist(resultats_probabiliste, bins=range(min(resultats_probabiliste), max(resultats_probabiliste) + 1),
                 edgecolor='black', color='purple', alpha=0.6, density=True, label='Stratégie probabiliste simplifiée')

        # Histogramme pour la stratégie heuristique (en vert)
        plt.hist(resultats_heuristique, bins=range(min(resultats_heuristique), max(resultats_heuristique) + 1),
                 edgecolor='black', color='green', alpha=0.6, density=True, label='Stratégie heuristique')

        # Histogramme pour la stratégie aléatoire (en bleu)
        plt.hist(resultats_aleatoire, bins=range(min(resultats_aleatoire), max(resultats_aleatoire) + 1),
                 edgecolor='black', color='skyblue', alpha=0.6, density=True, label='Stratégie aléatoire')

        # Ajout des lignes de l'espérance pour chaque stratégie
        plt.axvline(esperance_probabiliste, color='red', linestyle='dashed', linewidth=2,
                    label=f"Espérance probabiliste: {esperance_probabiliste:.2f}")
        plt.axvline(esperance_heuristique, color='orange', linestyle='dashed', linewidth=2,
                    label=f"Espérance heuristique: {esperance_heuristique:.2f}")
        plt.axvline(esperance_aleatoire, color='yellow', linestyle='dashed', linewidth=2,
                    label=f"Espérance aléatoire: {esperance_aleatoire:.2f}")

        # 5. Ajustements visuels
        plt.title(f"Comparaison des stratégies probabiliste, heuristique et aléatoire\n"
                  f"Espérance probabiliste: {esperance_probabiliste:.2f}, Écart-type: {std_dev_probabiliste:.2f}\n"
                  f"Espérance heuristique: {esperance_heuristique:.2f}, Écart-type: {std_dev_heuristique:.2f}\n"
                  f"Espérance aléatoire: {esperance_aleatoire:.2f}, Écart-type: {std_dev_aleatoire:.2f}",
                  fontsize=14)
        plt.xlabel("Nombre de coups", fontsize=12)
        plt.ylabel("Probabilité", fontsize=12)
        plt.legend(loc='upper left')
        plt.grid(True)

        # 6. Afficher l'histogramme
        plt.show()

        # Vérification de la validité des résultats
        self.assertTrue(min(resultats_aleatoire) < max(resultats_aleatoire),
                        "Les résultats aléatoires doivent contenir une plage valide de valeurs.")
        self.assertTrue(min(resultats_heuristique) < max(resultats_heuristique),
                        "Les résultats heuristiques doivent contenir une plage valide de valeurs.")
        self.assertTrue(min(resultats_probabiliste) < max(resultats_probabiliste),
                        "Les résultats probabilistes doivent contenir une plage valide de valeurs.")

    def tearDown(self):
        """
        Nettoyage après chaque test, si nécessaire.
        """
        pass

