######### CLASSE BATAILLE #########
import tkinter as tk

from .Config import HORIZONTAL, VERTICAL
from .GrilleMathematique import GrilleMathematique
from .Joueur import Joueur


class Bataille:
    """
        Classe principale pour gérer une partie de bataille navale.
        Contient une grille et les méthodes pour jouer, vérifier la victoire et réinitialiser le jeu.
        """

    def __init__(self, x, y, liste_bateaux):
        self.grille = GrilleMathematique(x, y)
        self.liste_bateaux = liste_bateaux
        self.grille.genere_grille(liste_bateaux)
        self.joueur = Joueur(self)

    @property
    def Grille(self):
        return self.grille

    def joue(self, type_jouee):
        # Diccionario "switch-case" que asocia un tipo de jugada con el método correspondiente
        switcher = {
            "aleatoire": self.joueur.simuler_aleatoire,
            "heuristique": self.joueur.jouee_heuristique,
            "probabiliste_simplifiee": self.joueur.jouee_probabiliste_simplifiee,
        }

        # Obtener la función correspondiente del diccionario
        func = switcher.get(type_jouee, None)

        # Si existe una función para el tipo de jugada especificada, se ejecuta
        if func:
            return func()  # Llama al método correspondiente
        else:
            raise ValueError(f"Type de coup '{type_jouee}' non reconnu.")

    def victoire(self):
        """
        Vérifie si tous les bateaux ont été coulés. Un bateau est coulé quand toutes ses cases sont touchées.
        :return: True si tous les bateaux sont coulés, sinon False.
        """
        return self.grille.cases_restantes == 0


    def reset(self):
        """
        Réinitialise la grille pour recommencer une nouvelle partie.
        """
        self.grille.reset()
        self.grille.genere_grille(self.liste_bateaux)  # Genera una nueva cuadrícula aleatoria de barcos

    def liste_bateaux_restants(self):
        """
        Renvoie la liste des bateaux qui ne sont pas encore complètement coulés.
        """
        bateaux_restants = []
        x_max, y_max = self.grille.x, self.grille.y  # Limites de la grille

        for bateau in self.liste_bateaux:
            est_coule = True  # On suppose que le bateau est coulé, on vérifiera case par case
            x_init, y_init = bateau.position
            longueur = bateau.longueur
            orientation = bateau.orientation

            # Parcourir toutes les cases que le bateau occupe
            for i in range(longueur):
                if orientation == HORIZONTAL:
                    x, y = x_init + i, y_init  # Si le bateau est horizontal, il s'étend vers la droite
                elif orientation == VERTICAL:
                    x, y = x_init, y_init + i # Si le bateau est vertical, il s'étend vers le bas

                # Vérifier si cette case a été révélée ou non
                if not self.grille.is_revealed(x, y):
                    est_coule = False
                    break  # Dès qu'on trouve une case non révélée, le bateau n'est pas coulé

            if not est_coule:
                bateaux_restants.append(bateau)

        return bateaux_restants

