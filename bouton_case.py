"""
Module contenant la description de la classe BoutonCase, ces bouton son généré par le module tkinter et font partie du jeu de démineur.

Auteurs: Frédéric Fiset-Tremblay et Charles-Albert Raymond
"""

from tkinter import Button

class BoutonCase(Button):
    """Cette classe regroupe tout ce qui concerne les attributs des cases ainsi que les méthodes qui serveront
        à les changer.

    Args:
        Button : Prend les attributs de la classe bouton de Tkinter.
        rangee_x : Rangée du grillage du jeu de démineur.
        colonne_y : Colonne du grillage du jeu de démineur.
    """
    def __init__(self, parent, rangee_x, colonne_y):
        """
        Constructeur de la classe avec des valeures par défauts.
        """
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        super().__init__(parent, text='\U0001F30D', padx=1, pady=3, height=1, width=2)

    def nouvelle_partie(self):
        """
        Initie les valeures des cases à la valeure de base.
        """
        self['text'] = '\U0001F30D'
        self.modifier_couleur('black')

    def modifier_couleur(self, couleur_texte):
        """
        Méthode qui modifie la couleur du texte pour la couleur donné en argument.
        """
        self['foreground'] = couleur_texte

    def est_mine(self):
        """
        Méthode qui modifie une case pour mettre un "emoji" de mine.
        """
        self['text'] = '\U0001F4A3'

    def marquer(self):
        """
        Méthode qui modifie une case pour mettre un "emoji" de marquage.
        """
        self['text'] = '\U0001F9E0'
        self.modifier_couleur('red')

    def demarquer(self):
        """
        Méthode qui modifie une case pour enlever la marque d'une case.
        """
        self.nouvelle_partie()
        
    def couleur_chiffre (self, chiffre): 
        """
        Méthode qui modifie la couleur des chiffres selon leur valeur.
        """
        if chiffre == 0 : 
            self.modifier_couleur('black')
        elif chiffre == 1 :
            self.modifier_couleur('green')
        elif chiffre == 2 :
            self.modifier_couleur('blue')
        elif chiffre == 3 :
            self.modifier_couleur('orange')
        elif chiffre == 4 : 
            self.modifier_couleur('red')
        else:
            self.modifier_couleur('brown')

