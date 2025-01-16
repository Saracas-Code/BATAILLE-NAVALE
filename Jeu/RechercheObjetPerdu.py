import random

class RechercheObjetPerdu:
    def __init__(self, grille, pi, ps, position_objet):
        """
        Initialise les paramètres de la recherche bayésienne
        grille: objet représentant la grille du jeu (grille déjà initialisée)
        pi: liste des probabilités a priori pour chaque case
        ps: probabilité de détection par le senseur
        position_objet: la position où l'objet se trouve (géré par la grille)
        """
        self.grille = grille
        self.pi = pi 
        self.ps = ps  
        self.position_objet = position_objet  

    def detecter(self, case):
        """
        Simule la détection dans une case avec probabilité ps.
        Renvoie 1 si l'objet est détecté, 0 sinon.
        """
        x = case // self.grille.y
        y = case % self.grille.y

        if self.grille.case_contient_objet((x, y)) and random.random() < self.ps:
            return 1  
        else:
            return 0  

    def mettre_a_jour_probabilites(self, case, detection):
        """
        Met à jour les probabilités bayésiennes après un sondage.
        """
        if detection == 0:  
            # Mise à jour de la probabilité pour la case sondée
            self.pi[case] = (1 - self.ps) * self.pi[case] / ((1 - self.ps) * self.pi[case] + (1 - self.pi[case]))

            # Mise à jour des probabilités des autres cases
            for i in range(len(self.pi)):
                if i != case:
                    self.pi[i] = self.pi[i] / (1 - self.pi[case] * (1 - self.ps))

    def recherche(self):
        """
        Algorithme de recherche d'objet perdu avec un senseur imparfait.
        Renvoie la position (x, y) de l'objet trouvé et le nombre de coups nécessaires.
        """
        nombre_coups = 0  # Initialisation du compteur de coups
        
        while True:

            nombre_coups += 1

            case = max(range(len(self.pi)), key=lambda i: self.pi[i])
            
            detection = self.detecter(case)
            
            if detection == 1:
                x = case // self.grille.y
                y = case % self.grille.y
                print(f"Objet trouvé en case ({x}, {y}) après {nombre_coups} coups.")
                return (x, y), nombre_coups  

            self.mettre_a_jour_probabilites(case, detection)



