######### CLASSE GRILLE #########
import random
import time
import numpy as np

from Jeu.Bateau import Bateau
from Jeu.Config import HORIZONTAL, VERTICAL, longueurs_bateaux


class GrilleMathematique:
    """
    Représente une grille de bataille navale avec des fonctionnalités pour afficher, comparer et générer des configurations de bateaux.
    """

    def __init__(self, x, y):

        self.__x = x
        self.__y = y
        self.__grille = np.zeros((y, x), dtype=int)  # numpy array
        self.__revealed = np.zeros((y, x), dtype=bool) # numpy array for the revealed cases
        self.cases_restantes = 0

    def reset(self):
        self.__grille.fill(0)
        self.__revealed.fill(False)
        self.cases_restantes = 0

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def taille_grille(self):
        return self.x * self.y

    @property
    def grille(self):
        return self.__grille

    def case(self, x, y):
        return self.__grille[x, y]

    def is_revealed(self, x, y):
        return self.__revealed[x, y]

    def revele_case(self, x, y):
        """
        Change l'état d'une case à révélé (True).
        """
        self.__revealed[x, y] = True

    def set_case(self, x, y, v):
        self.__grille[x, y] = v

    def tirer(self, position):

        # Obtenir les ordonnées
        x = position[0]
        y = position[1]

        # Rien faire si la case est déjà révélée
        if self.is_revealed(x, y):
            return False

        # Révéler la case
        self.revele_case(x, y)

        # Obtenir la valeur réelle de la case
        valor = self.case(x, y)

        if valor > 0:
            self.cases_restantes -= 1
            for i in range(self.x) :
                for j in range(self.y) :
                    if not self.is_revealed(i, j) : return "touché"
            return "coulé"
        return "raté"

    def eq(self, grilleB):
        """
        Compare la grille actuelle avec une autre grille `grilleB`.
        Retourne `True` si elles sont égales, sinon `False`.

        :param grilleB: L'autre grille à comparer avec la grille actuelle.
        :return: True si les deux grilles sont identiques, False sinon.
        """
        if not (self.x == grilleB.x and self.y == grilleB.y):
            return False
            # Comparer les grilles avec numpy array_equal
        if not np.array_equal(self.__grille, grilleB.grille):
            return False
        return True

    def genere_grille(self, listeBateaux):
        """
        Réinitialise la grille puis place aléatoirement les bateaux
        de la liste de bateaux
        """
        self.reset()
        for bateau in listeBateaux:
            bateau.place_alea(self)
            self.cases_restantes += longueurs_bateaux[bateau.id]
    
    # EXERCICE 3 COMBINATOIRE
    def nb_liste_bateaux(self, listeBateaux):
        """
        Calcule de manière récursive le nombre de configurations possibles
        d'une liste de bateaux sur la grille.

        :param listeBateaux: Liste des bateaux à placer sur la grille.
        :return: Nombre total de configurations possibles pour cette liste de bateaux.
        """
        if not listeBateaux:
            return 1  # Grille vide

        bateau = listeBateaux[0]
        count = 0

        # Parcourt toutes les positions possibles pour chaque bateau de façon récursif
        for i in range(self.x):
            for j in range(self.y):
                # Essaye de placer le bateau horizontalement
                if bateau.peut_placer(self, (i, j), HORIZONTAL):
                    bateau.place(self, (i, j), HORIZONTAL)
                    count += self.nb_liste_bateaux(listeBateaux[1:])
                    bateau.enlever(self) # On revient à l'arbre de recherche

                # Essaye de placer le bateau verticalement
                if bateau.peut_placer(self, (i, j), VERTICAL):
                    bateau.place(self, (i, j), VERTICAL)
                    count += self.nb_liste_bateaux(listeBateaux[1:])
                    bateau.enlever(self) # On revient à l'arbre de recherche

        return count

    # EXERCICE 4 COMBINATOIRE
    def prob_grille(self, listeBateaux, max_attempts=1000000, timeout=300):
        """
        Génère des grilles aléatoires jusqu'à ce qu'une grille égale à self soit trouvée,
        ou jusqu'à ce qu'un timeout ou un nombre maximum de tentatives soit atteint.

        :param max_attempts: Le nombre maximum de tentatives avant d'arrêter. Par défaut à 1 million.
        :param timeout: Le nombre maximum de secondes à attendre avant d'arrêter. Par défaut 300 secondes.
        :return: Le nombre de grilles générées avant de trouver la grille cible, ou -1 en cas d'échec.
        """
        grille = GrilleMathematique(self.x, self.y)
        count = 0
        start_time = time.time()  # Capture l'heure de début pour le timeout

        while count < max_attempts:
            count += 1
            if time.time() - start_time > timeout:  # Vérifie si le timeout est atteint
                print(f"Timeout atteint après {timeout} secondes et {count} tentatives.")
                return -1

            grille.genere_grille(listeBateaux)
            if grille.eq(self):
                break  # Sort de la boucle si les grilles sont identiques

        return count  # Retourne le nombre de tentatives nécessaires

    # EXERCICE 5 COMBINATOIRE
    def nb1_liste_bateaux(self, listeBateaux):
        """
        Calcule une approximation du nombre total de configurations possibles pour une liste de bateaux.

        :param listeBateaux: Liste des bateaux à placer sur la grille.
        :return: Nombre total approximatif de configurations possibles.
        """
        total_configurations = 1

        # Multiplie les configurations possibles pour chaque bateau
        for bateau in listeBateaux:
            total_configurations *= bateau.nb_bateau(self)

        return total_configurations

    # EXERCICE 6 COMBINATOIRE
    def nb2_liste_bateaux(self, listeBateaux):
        """ Renvoie une approximation du nombre de grilles différentes possibles
        contenant la liste de bateaux passée en paramètre.

        Une manière consiste à calculer le nombre de grilles possibles en plaçant le
        premier bateau, puis placer ce bateau dans une nouvelle grille, puis
        calculer le nombre de grilles possibles en plaçant le second bateau dans
        cette nouvelle grille et ainsi de suite.
        """
        res = 1
        grilleCour = GrilleMathematique(10, 10)
        for i in listeBateaux:
            res *= i.nb_bateau(grilleCour)
            i.place_alea(grilleCour)

        return res

    def bateau_coule(self, tir_suivant):
        """
        Vérifie si un bateau est coulé après un tir.
        :param tir_suivant: Tuple (x, y) représentant la case tirée.
        :return: True si le bateau est coulé, False sinon.
        """
        x, y = tir_suivant
        bateau_id = self.case(x, y)  # Identifiant du bateau sur cette case

        if bateau_id == 0:  # Si c'est de l'eau (aucun bateau), rien à vérifier
            return False

        # Vérifier toutes les cases de la grille pour ce bateau
        for i in range(self.x):
            for j in range(self.y):
                if self.case(i, j) == bateau_id and not self.is_revealed(i, j):
                    # Si on trouve une case de ce bateau qui n'est pas encore révélée, il n'est pas coulé
                    return False

        # Si toutes les cases du bateau sont révélées, alors il est coulé
        return True

    # PARTIE 4
    def positionner_objet(self):
        """
        Positionne l'objet de manière aléatoire dans la grille et retourne la position.
        """
        position_x = random.randint(0, self.x - 1)
        position_y = random.randint(0, self.y - 1)
        self.grille[position_x][position_y] = 1  # Marque la case où l'objet est placé
        return position_x, position_y

    def case_contient_objet(self, case):
        """
        Vérifie si une case contient l'objet.
        case: un index linéaire ou un tuple (x, y)
        """
        if isinstance(case, int):
            x = case // self.y  # Ligne (x)
            y = case % self.y  # Colonne (y)
        else:
            x, y = case

        return self.grille[x][y] == 1

