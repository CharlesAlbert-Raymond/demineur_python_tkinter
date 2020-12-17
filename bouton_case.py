"""
TODO: Ajoutez les docstrings et modifier le code au besoin.
"""

from tkinter import Button

class BoutonCase(Button):
    def __init__(self, parent, rangee_x, colonne_y):
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        super().__init__(parent, text='\U0001F30D', padx=1, pady=3, height=1, width=2)

    def nouvelle_partie(self):
        self['text'] = '\U0001F30D'
        self.modifier_couleur('black')

    def modifier_couleur(self, couleur_texte):
        self['foreground'] = couleur_texte

    def est_mine(self):
        self['text'] = '\U0001F4A3'

    def marquer(self):
        self['text'] = '\U0001F9E0'
        self.modifier_couleur('red')

    def demarquer(self):
        self['text'] = '\U0001F30D'
        self.modifier_couleur('black')
        
    def couleur_chiffre (self, chiffre): 
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

