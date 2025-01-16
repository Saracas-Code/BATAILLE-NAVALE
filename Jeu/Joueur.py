import random
import tkinter as tk
from tkinter import messagebox
import itertools as itr

from Jeu.Config import HORIZONTAL, VERTICAL


class Joueur:

    def __init__(self, bataille):
        """
        Initialise un joueur avec une instance de la bataille.
        """
        self.bataille = bataille

    def simuler_aleatoire(self, n=1000):
        resultats = []
        for _ in range(n):
            resultats.append(self.jouee_aleatoire())
        return resultats

    def jouee_aleatoire(self):
        # Compteur de coups
        nb_coups = 0
        tirs_joues = set()

        while not self.bataille.victoire():
            while True:
                x, y = random.randint(0, self.bataille.grille.x-1), random.randint(0, self.bataille.grille.x-1)
                if (x, y) not in tirs_joues:
                    tirs_joues.add((x, y))
                    self.bataille.grille.tirer((x, y))
                    nb_coups += 1
                    break
        self.bataille.reset()
        #print("Nombre de coups Aléatoire : " , nb_coups)
        return nb_coups

    def jouee_heuristique(self):
        """
        Stratégie heuristique pour couler les bateaux.
        - Si une case touchée contient une partie de bateau, tirer autour.
        - Sinon, tirer de manière plus intelligente en fonction de la grille.
        """
        nb_coups = 0
        tirs_joues = set()

        while not self.bataille.victoire():
            # Recherche des positions déjà touchées pour cibler les tirs autour
            tir_suivant = None
            for x in range(self.bataille.grille.x):
                for y in range(self.bataille.grille.y):
                    if self.bataille.grille.case(x, y) > 0 and self.bataille.grille.is_revealed(x, y):  # Si la case est touchée
                        # Tenter de tirer autour de la case touchée
                        voisins = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                        for (nx, ny) in voisins:
                            if 0 <= nx < self.bataille.grille.x and 0 <= ny < self.bataille.grille.y:
                                if (nx, ny) not in tirs_joues:
                                    tir_suivant = (nx, ny)
                                    break
                    if tir_suivant:
                        break
                if tir_suivant:
                    break

            # Si aucune case adjacente à un bateau touché n'est trouvée, tirer au hasard
            if not tir_suivant:
                while True:
                    x, y = random.randint(0, self.bataille.grille.x-1), random.randint(0, self.bataille.grille.y-1)
                    if (x, y) not in tirs_joues:
                        tir_suivant = (x, y)
                        break

            # Effectuer le tir
            self.bataille.grille.tirer(tir_suivant)
            tirs_joues.add(tir_suivant)
            nb_coups += 1

        # Réinitialiser la bataille à la fin
        self.bataille.reset()
        #print("Nombre de coups Heuristique: " , nb_coups)
        return nb_coups

    def jouee_probabiliste_simplifiee(self):
        """
        Stratégie probabiliste simplifiée pour couler les bateaux.
        - Tirer en priorisant certaines zones basées sur une estimation simplifiée des probabilités.
        """
        nb_coups = 0
        tirs_joues = set()
        grille_probabilites = self.initialiser_probabilites_centrées(10, 10)

        while not self.bataille.victoire():
            # Choisir la case avec la probabilité la plus élevée (si toutes sont égales, choisir aléatoirement)
            max_prob = max(max(row) for row in grille_probabilites)
            candidats = [(x, y) for x in range(self.bataille.grille.x) for y in range(self.bataille.grille.y)
                         if grille_probabilites[x][y] == max_prob and (x, y) not in tirs_joues]

            # Si des cases avec une probabilité maximale existent, tirer sur l'une d'elles
            if candidats:
                tir_suivant = random.choice(candidats)
            else:
                # Si toutes les probabilités sont égales, tirer au hasard sur une case non jouée
                while True:
                    x, y = random.randint(0, self.bataille.grille.x - 1), random.randint(0, self.bataille.grille.y - 1)
                    if (x, y) not in tirs_joues:
                        tir_suivant = (x, y)
                        break

            # Effectuer le tir
            res = self.bataille.grille.tirer(tir_suivant)
            tirs_joues.add(tir_suivant)
            nb_coups += 1

            # Mettre à jour la grille de probabilités
            grille_probabilites[tir_suivant[0]][tir_suivant[1]] = 0  # Réduire à 0 les cases déjà visitées
            if res == "raté" :
                self.diminuer_probabilites_adjacentes(tir_suivant, grille_probabilites, 10, 10,
                                                      0.9)  # Réduire 10% en adjacentes
                # Si el disparo fue un éxito (barco tocado)
            elif res == "touché":
                self.augmenter_probabilites_adjacentes(tir_suivant, grille_probabilites, 10, 10,
                                                        5)  # Augmenter probabilité en adjacentes

        self.bataille.reset()
        # print("Nombre de coups probabiliste simplifiée : " , nb_coups)
        return nb_coups

    def initialiser_probabilites_centrées(self, x_max, y_max):
        """
        Inicializa la grilla de probabilidades con valores más altos en el centro y más bajos en los bordes.
        """
        centro_x, centro_y = x_max // 2, y_max // 2
        max_dist = max(centro_x, centro_y)
        grille_probabilites = [[0 for _ in range(y_max)] for _ in range(x_max)]

        for x in range(x_max):
            for y in range(y_max):
                # Calculer la distance au centre
                dist_centro = ((x - centro_x) ** 2 + (y - centro_y) ** 2) ** 0.5
                grille_probabilites[x][y] = 1 / (1 + dist_centro / max_dist)

        # probabilités jusqu'a 100
        max_prob = max(max(row) for row in grille_probabilites)
        for x in range(x_max):
            for y in range(y_max):
                grille_probabilites[x][y] = int(grille_probabilites[x][y] / max_prob * 100)

        return grille_probabilites

    def augmenter_probabilites_adjacentes(self, tir_suivant, grille_probabilites, x_max, y_max, increment):
        """
        Augmente les probabilités des cases adjacentes à un tir réussi.
        """
        x, y = tir_suivant
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < x_max and 0 <= ny < y_max:
                grille_probabilites[nx][ny] += increment


    def diminuer_probabilites_adjacentes(self, tir_suivant, grille_probabilites, x_max, y_max, facteur_reduction):
        """
        Diminue les probabilités des cases adjacentes à un tir raté ou un bateau coulé.
        """
        x, y = tir_suivant
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < x_max and 0 <= ny < y_max:
                grille_probabilites[nx][ny] *= facteur_reduction  # Réduire de 10% (facteur_reduction = 0.9)