import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Jeu.Bateau import Bateau
from Jeu.GrilleGraphique import GrilleGraphique

# Créer la fenêtre principale
root = tk.Tk()
root.title("Test Grille Graphique")
root.attributes('-fullscreen', True)  # Mettre la fenêtre en plein écran

# Créer une grille de 10x10
grille = GrilleGraphique(10, 10)

# Créer une étiquette pour afficher le nombre de tours
turnos_label = tk.Label(root, text="Tours: 0", font=("Helvetica", 20))
turnos_label.pack(side=tk.TOP)

# Lier l'étiquette des tours à la classe GrilleGraphique
grille.tours_label = turnos_label

# Générer quelques bateaux de test et les placer aléatoirement sur la grille
liste_bateaux = [Bateau(1), Bateau(2), Bateau(3), Bateau(4), Bateau(5)]  # Cinq bateaux de tailles différentes
grille.genere_grille(liste_bateaux)

# Afficher la grille dans une fenêtre Tkinter avec matplotlib
grille.affiche(root)

# Créer un canvas pour insérer la figure matplotlib dans Tkinter
canvas = FigureCanvasTkAgg(grille.fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Créer un bouton pour fermer la fenêtre
button = tk.Button(root, text="Quitter", command=root.quit, width=10, height=2, font=("Helvetica", 15))
button.pack(side=tk.BOTTOM)

# Démarrer la boucle principale des événements de Tkinter
tk.mainloop()
