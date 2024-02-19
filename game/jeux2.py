import random


class Carte:
    figure = {11: "Valet", 12: "Dame", 13: "Roi", 14: "As"}
    color = ('Trèfle', 'Pique', 'Coeur', 'Carreau')

    def __init__(self, v, c):
        self.valeur = v
        self.couleur = c

    def __str__(self):
        if self.valeur > 10:
            return (Carte.figure[self.valeur] + " de " + self.couleur)
        else:
            return (str(self.valeur) + " de " + self.couleur)

    def compare(self, x):
        if self.valeur < x.valeur:
            return ("-1")
        if self.valeur == x.valeur:
            return ("0")
        if self.valeur > x.valeur:
            return ("+1")


class Joueur:
    def __init__(self, n, s, t):
        self.nom = n
        self.score = s
        self.tas = t

    def __str__(self):
        return (self.nom + " a " + str(self.score) + " point(s)")


class Point:
    def point(self, chiffre):
        '''
        permet de d'ajouter 10 si une carte correspond à 11/12/13 et de crée une exception pour l'As
        '''
        un = 0
        if chiffre == 11 or chiffre == 12 or chiffre == 13:
            chiffre = 10
            return chiffre
        elif chiffre == 14:
            chiffre = 14
            return chiffre
        else:
            return chiffre


class carte:
    def randomC(self, ctx):
        """
        permet d'initialiser une carte
        """
        a = 1
        color = ("Trèfle", "Pique", "Coeur", "Carreau")
        chiffres = random.randint(2, 14)
        couleur = (random.choice(color))
        chiffre = Point.point(self, chiffres)
        return chiffres, chiffre, couleur, a

    def testAs(self, ctx, chiffre, a):
        """
        permet de compter e nombre d'As
        """
        if chiffre == 14:
            a = a + 1
        return a

    def verifAs(self, ctx, joueur, j):
        """
        permet de sélectioner le meilleur choix pour l'As
        """

        if j > 0:
            joueur = joueur - (j * 14)
            while j > 0:
                if joueur + 11 < 22:
                    joueur = joueur + 11
                    j = j - 1
                elif joueur + 1 < 22:
                    joueur = joueur + 1
                    j = j - 1
                else:
                    joueur = joueur + 1
                    j = j - 1
        return joueur












