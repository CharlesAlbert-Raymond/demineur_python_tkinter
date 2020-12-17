"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""
from tkinter import Tk, Frame, Button, messagebox
from tableau import Tableau
from bouton_case import BoutonCase
from case import Case

class InterfacePartie(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0,0)

        self.tableau_mines = Tableau()

        bouton_frame = Frame(self)
        bouton_frame.grid()

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0)

        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quitter)
        bouton_quitter.grid(row=0, column=1)

        bouton_parametre = Button(bouton_frame, text='Paramètre', command=self.parametre)
        bouton_parametre.grid(row=0, column=3)

        self.cadre = Frame(self)
        self.cadre.grid(padx=20, pady=20)

        self.dictionnaire_boutons = {}
    
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<ButtonRelease-1>', self.devoiler_case)
                bouton.bind('<ButtonRelease-3>', self.marquer_case)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton


        bouton_sauvegarder = Button(bouton_frame, text='Sauvegarder', command=self.sauvegarde)
        bouton_sauvegarder.grid(row=1, column=0)

        bouton_charger = Button(bouton_frame, text='Charger une partie', command=self.charger)
        bouton_charger.grid(row=1, column=1)

    def devoiler_case(self, event):
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if case.est_minee:
            BoutonCase.est_mine(bouton)
            self.partie_terminer(False)
        else:
            self.devoiler_case_automatique(bouton.rangee_x, bouton.colonne_y)

    def marquer_case(self, event):
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if not case.est_devoilee and not case.est_marquee:
            BoutonCase.marquer(bouton)
            case.marquee()
        elif not case.est_devoilee and case.est_marquee:
            BoutonCase.demarquer(bouton)
            case.demarquee()

    def devoiler_case_automatique(self, rangee_x, colonne_y):
        bouton = self.dictionnaire_boutons[(rangee_x, colonne_y)]
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if not case.est_minee:
            bouton.modifier_couleur('black')
            bouton['text'] = case.nombre_mines_voisines
            if not case.est_devoilee:
                case.est_devoilee = True
                self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1
                if self.tableau_mines.nombre_cases_sans_mine_a_devoiler == 0:
                    self.partie_terminer(True)
                if case.nombre_mines_voisines == 0:
                    cases_voisines = self.tableau_mines.obtenir_voisins(rangee_x, colonne_y)
                    for voisins in cases_voisines:
                        self.devoiler_case_automatique(voisins[0], voisins[1])

    def parametre(self):
        pass

    def sauvegarde(self):
        pass

    def charger(self):
        pass

    def nouvelle_partie(self):
        self.tableau_mines = Tableau()

        for bouton in self.dictionnaire_boutons.values():
            BoutonCase.nouvelle_partie(bouton)

    def quitter(self):
        MsgBox = messagebox.askquestion("Quitter?", "Voulez-vous vraiment quitter?", icon="warning")
        if MsgBox == 'yes':
            self.quit()
        

    def partie_terminer(self, victoire):

        for case in self.tableau_mines.dictionnaire_cases.keys():
            bouton = self.dictionnaire_boutons[case]
            if self.tableau_mines.dictionnaire_cases[case].est_minee:
                BoutonCase.est_mine(bouton)
            else:
                bouton['text'] = self.tableau_mines.dictionnaire_cases[case].nombre_mines_voisines


        if victoire:
            text_fin = "Victoire!"
        else:
            text_fin = "Défaite :("

        MsgBox = messagebox.askquestion(text_fin, 'Voulez-vous commencer une autre partie?',
                                           icon='warning')
        if MsgBox == 'yes':
            self.nouvelle_partie()
        else:
            self.quit()