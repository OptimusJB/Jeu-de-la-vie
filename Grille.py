import random

class Grille:
    def __init__(self, dimension):
        self.grille = []
        self.dimension = dimension
        for i in range(dimension):
            liste = []
            for u in range(dimension):
                liste.append(False)
            self.grille.append(liste)
        
    def __str__(self):
        chaine = ""
        for ligne in self.grille:
            new_liste = []
            dico = {True:1, False:0}
            for element in ligne:
                new_liste.append(dico[element])
                
            chaine = chaine + "\n" + str(new_liste)
        return chaine
    
    def melanger(self):
        for y in range(len(self.grille)):
            for x in range(len(self.grille)):
                self.set_valeur(x, y, random.choice([True, False]))
        
    def est_vivant(self, x, y):
        #print(self)
        return self.grille[y][x] == True
    
    def check_exist(self, x, y):
        # retourne True si le voisin existe et est vivant
        if 0 <= x <= len(self.grille) - 1 and 0 <= y <= len(self.grille) - 1:
            if self.est_vivant(x, y):
                return True
        return False
    
    def set_valeur(self, x, y, valeur:bool):
        self.grille[y][x] = valeur
    
    def nb_voisins_vivants(self, x, y):
        liste_voisins = [self.check_exist(x-1, y-1),
                         self.check_exist(x, y - 1),
                         self.check_exist(x + 1, y - 1),
                         self.check_exist(x - 1, y),
                         self.check_exist(x + 1, y),
                         self.check_exist(x - 1, y + 1),
                         self.check_exist(x, y + 1),
                         self.check_exist(x + 1, y + 1)]
        #print("-", x, y, liste_voisins)
        #print(x, y, liste_voisins.count(True))
        return liste_voisins.count(True)
    
    def copy_grille(self, grille):
        new_grille = []
        for ligne in grille:
            new_grille.append(list(ligne))
        return new_grille
    
    def next_turn(self):
        # nouvelle grille
        new_grille = self.copy_grille(self.grille)
        #print(new_grille)
        for y in range(len(self.grille)):
            for x in range(len(self.grille)):
                nb_voisins = self.nb_voisins_vivants(x, y)
                if not self.est_vivant(x, y):
                    if nb_voisins == 3:
                        #print(x,y)
                        new_grille[y][x] = True
                        #print(new_grille == self.grille)
                        #print(self)
                else:
                    if not 2 <= nb_voisins <= 3:
                        new_grille[y][x] = False
        self.grille = self.copy_grille(new_grille)