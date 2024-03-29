# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Tableau. Un tableau est utilisé pour jouer une partie du jeu Démineur.

Auteurs: Frédéric Fiset-Tremblay et Charles-Albert Raymond
"""

from case import Case
from random import randint


class Tableau():
    """
    Tableau du jeu de démineur, implémenté avec un dictionnaire de cases.

    Warning:
        Si vous ajoutez des attributs à la classe Tableau, n'oubliez pas de les documenter ici.

    Attributes:
        dimension_rangee (int): Nombre de rangées du tableau
        dimension_colonne (int): Nombre de colonnes du tableau
        nombre_mines (int): Nombre de mines cachées dans le tableau

        nombre_cases_sans_mine_a_devoiler (int) : Nombre de cases sans mine qui n'ont pas encore été dévoilées
            Initialement, ce nombre est égal à dimension_rangee * dimension_colonne - nombre_mines

        dictionnaire_cases (dict): Un dictionnaire de case en suivant le format suivant:
            Les clés sont les positions du tableau sous la forme d'un tuple (x, y),
                x étant le numéro de la rangée, y étant le numéro de la colonne.
            Les éléments sont des objets de la classe Case.
    """

    def __init__(self, dimension_rangee=5, dimension_colonne=5, nombre_mines=5):
        """ Initialisation d'un objet tableau.

        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau (valeur par défaut: 5)
            dimension_colonne (int): Nombre de colonnes du tableau (valeur par défaut: 5)
            nombre_mines (int): Nombre de mines cachées dans le tableau (valeur par défaut: 5)
        """

        self.dimension_rangee = dimension_rangee
        self.dimension_colonne = dimension_colonne
        self.nombre_mines = nombre_mines

        # Le dictionnaire de case, vide au départ, qui est rempli par la fonction initialiser_tableau().
        self.dictionnaire_cases = {}

        self.initialiser_tableau()

        self.nombre_cases_sans_mine_a_devoiler = self.dimension_rangee * self.dimension_colonne - self.nombre_mines

    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Valide les coordonnées reçues en argument. Les coordonnées sont considérées valides si elles se trouvent bien
        dans les dimensions du tableau.

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées

        Returns:
            bool: True si les coordonnées (x, y) sont valides, False autrement
        """
        rangee_valide = rangee_x >= 1 and rangee_x <= self.dimension_rangee
        colonne_valide = colonne_y >= 1 and colonne_y <= self.dimension_colonne
        return rangee_valide and colonne_valide

    def obtenir_case(self, rangee_x, colonne_y):
        """
        Récupère une case à partir de ses numéros de ligne et de colonne

        Args:
            rangee_x (int) : Numéro de la rangée de la cas
            colonne_y (int): Numéro de la colonne de la case
        Returns:
            Case: Une référence vers la case obtenue
            (ou None si les coordonnées ne sont pas valides)
        """
        if not self.valider_coordonnees(rangee_x, colonne_y):
            return None

        coordonnees = (rangee_x, colonne_y)
        return self.dictionnaire_cases[coordonnees]

    def obtenir_voisins(self, rangee_x, colonne_y):
        """
        Retourne une liste de coordonnées correspondant aux cases voisines d'une case. Toutes les coordonnées retournées
        doivent être valides (c'est-à-dire se trouver à l'intérieur des dimensions du tableau).

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut connaître les cases voisines
            colonne_y (int): Numéro de la colonne de la case dont on veut connaître les cases voisines

        Returns:
            list : Liste des coordonnées (tuple x, y) valides des cases voisines de la case dont les coordonnées
            sont reçues en argument
        """
        voisinage = ((-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, 1),
                     (1, -1), (1, 0), (1, 1))

        liste_coordonnees_cases_voisines = []

        for coordonee_a_verifier in voisinage:
            voisin_x = rangee_x + coordonee_a_verifier[0]
            voisin_y = colonne_y + coordonee_a_verifier[1]
            if self.valider_coordonnees(voisin_x, voisin_y):
                liste_coordonnees_cases_voisines.append((voisin_x, voisin_y))
        return liste_coordonnees_cases_voisines

    def initialiser_tableau(self):
        """
        Initialise le tableau à son contenu initial en suivant les étapes suivantes:
            1) On crée chacune des cases du tableau (cette étape est programmée pour vous).
            2) On y ajoute ensuite les mines dans certaines cases qui sont choisies au hasard
                (attention de ne pas choisir deux fois la même case!).
                - À chaque fois qu'on ajoute une mine dans une case, on obtient la liste de
                  ses voisins (pour se faire, utilisez la méthode obtenir_voisins)
                - Pour chaque voisin, on appelle la méthode ajouter_une_mine_voisine de la case correspondante.
        """
        for rangee_x in range(1, self.dimension_rangee + 1):
            for colonne_y in range(1, self.dimension_colonne + 1):
                coordonnees = (rangee_x, colonne_y)
                self.dictionnaire_cases[coordonnees] = Case()

        # TODO: À compléter (étape 2)
        # Nous vous suggérons d'utiliser dans la fonction randint(a,b) du module random qui
        # retourne un entier aléatoire compris entre a et b inclusivement.

        # Choisi 2 entier au hasard pour l'axe x et l'axe y
        mine_placée = 0
        position_mine = []
        while not mine_placée == self.nombre_mines:
            x = randint(1, self.dimension_rangee)
            y = randint(1, self.dimension_colonne)
            coordonnees_mine = (x, y)

            # Voit si une bombe est déjà présente
            if coordonnees_mine in position_mine:
                pass  # Si présente on recherche 2 entiers

            # Si non présente on assigne une bombe à cet endroit
            else:
                position_mine.append(coordonnees_mine)

                self.dictionnaire_cases[coordonnees_mine].est_minee = True

                mine_placée += 1

                # On trouve chaque voisin
                voisins = self.obtenir_voisins(coordonnees_mine[0], coordonnees_mine[1])

                # À chaque voisin on lui dit qu'une mine est voisine (ajouter_une_mine_voisine)
                for i in voisins:
                    self.dictionnaire_cases[i].ajouter_une_mine_voisine()









    def contient_mine(self, rangee_x, colonne_y):
        """
        Méthode qui vérifie si la case dont les coordonnées sont reçues en argument contient une mine.

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut vérifier si elle contient une mine
            colonne_y (int): Numéro de la colonne de la case dont on veut vérifier si elle contient une mine

        Returns:
            bool: True si la case à ces coordonnées (x, y) contient une mine, False autrement.
        """
        if self.dictionnaire_cases[(rangee_x, colonne_y)].est_minee:
            return True
        else:
            return False


#### Tests unitaires (à compléter) ###

def test_initialisation():
    tableau_test = Tableau()

    assert tableau_test.nombre_cases_sans_mine_a_devoiler == tableau_test.dimension_colonne * \
           tableau_test.dimension_rangee - tableau_test.nombre_mines


def test_valider_coordonnees():
    tableau_test = Tableau()
    dimension_x, dimension_y = tableau_test.dimension_rangee, tableau_test.dimension_colonne

    assert tableau_test.valider_coordonnees(dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x + 1, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x, dimension_y + 1)
    assert not tableau_test.valider_coordonnees(-dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(0, 0)


def test_obtenir_voisins():
    assert tableau_test.obtenir_voisins(5, 5) == [(4, 4), (4, 5), (5, 4)]
    assert not tableau_test.obtenir_voisins(1, 1) == [(1, 2), (1, 3), (2, 1), (2, 2)]
    assert tableau_test.obtenir_voisins(0, 0) == [(1, 1)]
    assert tableau_test.obtenir_voisins(2, 2) == [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]


def test_case_contient_mine():
    for i in tableau_test.dictionnaire_cases:
        tableau_test.dictionnaire_cases[i].est_minee = False
    for i in tableau_test.dictionnaire_cases:
        assert tableau_test.contient_mine(i[0], i[1]) == False

    tableau_test.dictionnaire_cases[(1, 1)].est_minee = True
    assert tableau_test.contient_mine(1, 1)
    tableau_test.dictionnaire_cases[(2, 2)].est_minee = True
    assert tableau_test.contient_mine(2, 2)
    tableau_test.dictionnaire_cases[(3, 3)].est_minee = True
    assert tableau_test.contient_mine(3, 3)


if __name__ == '__main__':

    tableau_test = Tableau()

    print('Tests unitaires...')
    test_initialisation()
    test_valider_coordonnees()
    test_obtenir_voisins()
    test_case_contient_mine()
    print('Tests réussis!')