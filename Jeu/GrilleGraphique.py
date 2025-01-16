######### CLASSE GRILLE GRAPHIQUE #########
from tkinter import messagebox

import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.figure import Figure

from .Config import longueurs_bateaux


class GrilleGraphique:
    """
    Représente une grille de bataille navale avec des fonctionnalités pour afficher, comparer et générer des configurations de bateaux.
    """

    def __init__(self, x, y):

        self.__x = x
        self.__y = y
        self.__grille = np.zeros((y, x), dtype=int)  # numpy array
        self.__revealed = np.zeros((y, x), dtype=bool)  # numpy array de cases revelées
        self.cases_restantes = 0
        self.tours = 0

        ### Atributes pour la fênetre graphique ###
        self.hidden_color = '#d3d3d3' # Gris clair pour les cases cachées
        self.colors = ['#add8e6', 'red', 'green', 'yellow', 'orange', 'purple', 'blue']
        self.fig = None  # Figure Matplotib
        self.ax = None  # Axes Matplotib
        self.message_text = None  # Texto del mensaje en la figura
        self.tours_label = None


    def reset(self):
        self.__grille.fill(0)
        self.__revealed.fill(False)

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

    @property
    def shape(self):
        return self.__grille.shape

    def affiche(self, root):
        """
        Affiche graphiquement la grille initialement en gris. Les clics de l'utilisateur révèlent les couleurs
        """
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Affichage initial : toute la grille en gris (non révélée)
        display_grid = np.where(self.__revealed, self.__grille, -1)  # Montre les valeurs seulement si révélées, -1 pour non révélées
        cmap = ListedColormap([self.hidden_color] + self.colors)
        norm = BoundaryNorm(np.arange(-1.5, len(self.colors) - 0.5, 1), cmap.N)

        # Affiche la grille avec les valeurs révélées ou gris pour les cases non révélées
        self.image = self.ax.imshow(display_grid.T, cmap=cmap, norm=norm, origin='lower', extent=[0, self.__y, 0, self.__x])

        # Configure les axes et la grille
        self.ax.set_xticks(np.arange(0, self.__y, 1))
        self.ax.set_yticks(np.arange(0, self.__x, 1))
        self.ax.grid(which="both", color='black', linestyle='-', linewidth=2)
        self.ax.set_xlim(0, self.__y)
        self.ax.set_ylim(0, self.__x)

        # Connecter l'événement de clic
        self.fig.canvas.mpl_connect('button_press_event', lambda event: self.on_click(event, root))
        # Créer un lieu pour le message
        self.message_text = self.ax.text(0.5, -0.1, '', transform=self.ax.transAxes, ha="center", fontsize=14, color="black")

    def on_click(self, event, root):
        """
        Gestionnaire d'événements pour les clics sur la grille.
        Affiche uniquement la couleur et le numéro de la case cliquée.
        """
        if event.xdata is None or event.ydata is None:
            return  # Ignorer si el clic n'est pas dans los limites de la grille

        # Obtenir les ordonnées
        x = int(event.xdata)
        y = int(event.ydata)

        if 0 <= x < self.__x and 0 <= y < self.__y:

            # Rien faire si la case est déjà révélée
            if self.is_revealed(x, y):
                return

            # Révéler la case
            self.revele_case(x, y)

            # Obtenir la valeur réelle de la case
            valor = self.case(x, y)

            # Update la grille
            self.image.set_array(np.where(self.__revealed, self.__grille, -1).T)

            self.tours += 1
            if self.tours_label:
                self.tours_label.config(text=f"Tours: {self.tours}")

            # Mettre le texte informatif
            if valor > 0:
                self.message_text.set_text(f"Bateau touché!! Tu as cliqué sur la case: ({x}, {y}).")
                self.cases_restantes -= 1
            else:
                self.message_text.set_text(f"Case vide. Tu as cliqué sur la case: ({x}, {y}).")

            # Actualiser la colormap et la grille affichée
            self.image.set_cmap(ListedColormap([self.hidden_color] + self.colors))

            # Refresh
            self.fig.canvas.draw_idle()

            # Voir si le joueur a gagné
            if (self.cases_restantes != 0): return False
            messagebox.showinfo("Victoire", f"Félicitations ! Vous avez gagné en {self.tours} tours.")

            root.quit()
            root.destroy()

    def genere_grille(self, listeBateaux):
        """
        Réinitialise la grille puis place aléatoirement les bateaux
        de la liste de bateaux
        """
        self.reset()
        for bateau in listeBateaux:
            bateau.place_alea(self)
            self.cases_restantes += longueurs_bateaux[bateau.id]
