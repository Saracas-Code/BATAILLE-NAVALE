# Projet Bataille Navale - LU3IN005 Statistique et Informatique

Ce projet fait partie du cours LU3IN005 Statistique et Informatique, et il modélise un jeu de bataille navale avec plusieurs méthodes d'automatisation pour couler les bateaux. 

## Organisation du projet

Le projet est organisé en deux principaux paquets : **jeu** et **tests**.

### 1. Paquet **jeu**

Le paquet **jeu** contient toutes les classes nécessaires pour instancier et manipuler les objets de la bataille navale. Les classes définissent les composants essentiels tels que la grille, les bateaux, et les joueurs. Ces classes sont utilisées pour modéliser et exécuter une partie de bataille navale.

En plus des objets du jeu, le paquet inclut une classe dédiée à la gestion d'une recherche d'un objet perdu dans une grille. Cette partie fait partie de la dernière section du projet.

### 2. Paquet **tests**

Le paquet **tests** contient des tests automatisés qui valident le bon fonctionnement des diverses fonctions et stratégies implémentées dans le jeu.

#### Tests automatisés :
Le fichier **Test.py** exécute l'ensemble des tests d'un coup. Les différents tests implémentés sont les suivants :

- **Test combinatoire** : Ce test analyse le nombre de configurations possibles pour placer les 5 bateaux sur la grille de la bataille navale.
  
- **Tests de stratégies de jeu** : Le projet inclut plusieurs méthodes pour jouer automatiquement à la bataille navale. Les stratégies implémentées sont :
  - **Stratégie aléatoire** : Les tirs sont effectués de manière complètement aléatoire.
  - **Stratégie heuristique** : Une méthode basée sur des règles simples pour optimiser les tirs.
  - **Stratégie probabiliste simplifiée** : Une méthode basée sur une grille de probabilités pour maximiser les chances de toucher un bateau.

Les tests génèrent également des graphiques comparant les performances des différentes stratégies (en termes de nombre de coups) et fournissent des informations statistiques détaillées.

## Fichier **main.py**

Le fichier **main.py** est un script de démonstration qui utilise la fonction `affiche` pour visualiser la grille du jeu. L'objectif est d'offrir une interface graphique plus intuitive grâce à l'utilisation de bibliothèques telles que **Tkinter** et **Matplotlib** pour une meilleure qualité visuelle.

### Interface de jeu :
- La sélection des cases se fait via un clic de souris.
- Lorsqu'une case est sélectionnée, son contenu est révélé.
- Une fois que toutes les cases contenant des bateaux sont découvertes, un message de félicitations apparaît. En cliquant sur "OK", le programme se ferme.

## Graphiques et visualisations

Grâce à **Matplotlib**, nous avons intégré la génération de graphiques pour visualiser les performances des différentes stratégies de jeu. Cela permet d’analyser les résultats des tests et de comparer les différentes méthodes utilisées.

## Conclusion

Ce projet explore des concepts avancés en statistique et informatique appliqués à un jeu de bataille navale. À travers des stratégies variées, une interface graphique simple et des tests automatisés, nous avons cherché à modéliser et à analyser différentes approches pour résoudre ce problème classique.
