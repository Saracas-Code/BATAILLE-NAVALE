######### CLASSE BATEAU #########

import random
from .Config import longueurs_bateaux, HORIZONTAL, VERTICAL

class Bateau:
    """
    Représente un bateau dans le jeu de bataille navale.
    Chaque bateau a un ID, une longueur, une position et une orientation (horizontale ou verticale).
    """
    def __init__(self, id):
        self.__id = id
        self.__longueur = longueurs_bateaux[id]

    @property
    def position(self):
        return self.__position

    @property
    def id(self):
        return self.__id

    @property
    def longueur(self):
        return self.__longueur

    @property
    def orientation(self):
        return self.__orientation

    def peut_placer(self, grille, position, direction):
        """
        Vérifie si le bateau peut être placé à la position donnée sur la grille dans la direction donnée
        (sans chevaucher d'autres bateaux et sans dépasser les limites de la grille).

        :param grille: La grille sur laquelle le bateau doit être placé.
        :param position: Tuple (x, y) représentant la position de départ sur la grille.
        :param direction: Orientation du bateau (HORIZONTAL ou VERTICAL).
        :return: bool - Retourne True si le bateau peut être placé, sinon False.
        """
        x, y = position
        longueur = longueurs_bateaux[self.id]

        # Vérifier les contraintes pour la direction verticale
        if direction == VERTICAL:
            if y + longueur > grille.y:
                return False
            return all(grille.case(x, y + i) == 0 for i in range(longueur))

        # Vérifier les contraintes pour la direction horizontale
        elif direction == HORIZONTAL:
            if x + longueur > grille.x:
                return False
            return all(grille.case(x + i, y) == 0 for i in range(longueur))

        return False

    def place(self, grille, position, direction):
        """
        Place le bateau sur la grille à la position donnée dans la direction spécifiée,
        si l'emplacement est valide.

        :param grille: La grille sur laquelle le bateau doit être placé.
        :param position: Tuple (x, y) représentant la position de départ sur la grille.
        :param direction: Orientation du bateau (HORIZONTAL ou VERTICAL).
        :return: bool - Retourne True si le bateau a été placé avec succès, sinon False.
        """
        x, y = position
        if not self.peut_placer(grille, position, direction):
            return False

        longueur = longueurs_bateaux[self.id]

        # Placer le bateau en position verticale
        if direction == VERTICAL:
            for i in range(longueur):
                grille.set_case(x, y + i, self.id)

        # Placer le bateau en position horizontale
        elif direction == HORIZONTAL:
            for i in range(longueur):
                grille.set_case(x + i, y, self.id)

        self.__position = position
        self.__orientation = direction

        return True

    def enlever(self, grille):
        """
        Enlève le bateau de la grille, en remplaçant ses cases par des zéros (cases vides).

        :param grille: La grille depuis laquelle le bateau doit être enlevé.
        """
        x, y = self.position

        # Enlever le bateau placé horizontalement
        if self.orientation == HORIZONTAL:
            for i in range(longueurs_bateaux[self.id]):
                grille.set_case(x + i, y, 0)

        # Enlever le bateau placé verticalement
        elif self.orientation == VERTICAL:
            for i in range(longueurs_bateaux[self.id]):
                grille.set_case(x, y + i, 0)

    def place_alea(self, grille):
        """
        Place le bateau aléatoirement sur la grille, en choisissant une position et une orientation au hasard.

        :param grille: La grille sur laquelle le bateau doit être placé.
        """
        while True:
            # Générer des positions et des directions aléatoires
            position = random.randint(0, grille.x - 1), random.randint(0, grille.y - 1)
            direction = random.choice([HORIZONTAL, VERTICAL])
            # Essayer de placer le bateau à cette position et dans cette direction
            if self.place(grille, position, direction):
                break

    # EXERCICE 2 COMBINATOIRE
    def nb_bateau(self, grille):
        """
        Calcule le nombre de positions possibles pour ce bateau sur la grille
        en fonction de sa longueur, en prenant en compte les orientations horizontales et verticales.

        :param grille: La grille sur laquelle le bateau doit être placé.
        :return: int - Le nombre de positions possibles pour placer le bateau.
        """
        taille_grille_x, taille_grille_y = grille.x, grille.y

        # Compteur de positions valides
        positions_possibles = 0

        # Explorer toutes les positions pour la direction horizontale
        for x in range(taille_grille_x):
            for y in range(taille_grille_y):
                if self.peut_placer(grille, (x, y), HORIZONTAL):
                    positions_possibles += 1

        # Explorer toutes les positions pour la direction verticale
        for x in range(taille_grille_x):
            for y in range(taille_grille_y):
                if self.peut_placer(grille, (x, y), VERTICAL):
                    positions_possibles += 1

        return positions_possibles
