"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""
from tkinter import Tk, Frame, Button, messagebox, simpledialog, Label,  filedialog
from tableau import Tableau
from bouton_case import BoutonCase
from chaine_a_liste import chaine_a_liste
from case import Case

class InterfacePartie(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0,0)
        self.dimension_rangee, self.dimension_colonne, self.nombre_mines, self.nombre_de_tour = 0,0,0,0
        self.dictionnaire_boutons = {}
        self.tableau_mines = Tableau()

        bouton_frame = Frame(self)
        bouton_frame.grid()

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0, padx=5, pady=5)

        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quitter)
        bouton_quitter.grid(row=0, column=1, padx=5, pady=5)

        bouton_instruction = Button(bouton_frame, text='Instruction', command=self.instruction)
        bouton_instruction.grid(row=0, column=2, padx=5, pady=5)

        bouton_sauvegarder = Button(bouton_frame, text='Sauvegarder', command=self.sauvegarde)
        bouton_sauvegarder.grid(row=0, column=3, padx=5, pady=5)

        bouton_charger = Button(bouton_frame, text='Charger une partie', command=self.valider_charger_partie)
        bouton_charger.grid(row=0, column=4, padx=5, pady=5)

    def nouvelle_partie(self):

        self.demander_dimension()
        self.tableau_mines = Tableau(self.dimension_rangee, self.dimension_colonne, self.nombre_mines)

        self.cadre = Frame(self)
        self.cadre.grid(padx=20, pady=20)

        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)
                bouton.bind('<ButtonRelease-1>', self.devoiler_case)
                bouton.bind('<ButtonRelease-3>', self.marquer_case)
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton
        self.nombre_de_tour = 0

        self.compteur = Label(self.cadre)
        self.compteur.grid(row = self.tableau_mines.dimension_rangee +2 , column = self.tableau_mines.dimension_colonne +2)
        self.compteur['text']= "Nombre de tours : {}".format(self.nombre_de_tour)


    def devoiler_case(self, event):

        bouton = event.widget
        self.nombre_de_tour += 1
        self.compteur['text'] = "Nombre de tours : {}".format(self.nombre_de_tour)

        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if case.est_minee:
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

    def instruction(self):
        pass

    def sauvegarde(self):
        if self.dictionnaire_boutons == {}:
            messagebox.message(title='Erreur', message='Aucune partie en cours')

        nombre_range = self.dimension_rangee
        nombre_colonne = self.dimension_colonne
        nombre_tour = self.nombre_de_tour
        position_mines = []
        position_cases_devoilees = []
        position_cases_marquees = []
        for bouton in self.dictionnaire_boutons.values():
            case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
            if case.est_minee:
                position_mines.append((bouton.rangee_x, bouton.colonne_y))
            if case.est_devoilee:
                position_cases_devoilees.append((bouton.rangee_x, bouton.colonne_y))
            if case.est_marquee:
                position_cases_marquees.append((bouton.rangee_x, bouton.colonne_y))


        nom_fichier = filedialog.asksaveasfile(mode='w', defaultextension=".txt")

        nom_fichier.write(str(nombre_range)+"\n")
        nom_fichier.write(str(nombre_colonne)+"\n")
        nom_fichier.write(str(nombre_tour) + "\n")
        nom_fichier.write(str(position_mines)+"\n")
        nom_fichier.write(str(position_cases_devoilees)+"\n")
        nom_fichier.write(str(position_cases_marquees)+"\n")
        nom_fichier.close


    def valider_charger_partie(self):
        if self.dictionnaire_boutons != {}:
            msg = messagebox.askquestion(title='Attention', message="Votre partie sera effacée si elle n'est pas sauvegarder", icon="warning")
            if msg == 'yes':
                self.cadre.destroy()
                self.charger()
        else :
            self.charger()

    def charger(self):


        nom_fichier = filedialog.askopenfile(mode="r", defaultextension=".txt")

        self.dimension_rangee = int(nom_fichier.readline())
        self.dimension_colonne = int(nom_fichier.readline())
        self.nombre_de_tour = int(nom_fichier.readline())
        position_mines = chaine_a_liste(list(nom_fichier.readline().strip('\n')))
        position_cases_devoilees = chaine_a_liste(nom_fichier.readline().strip('\n'))
        position_cases_marquees = chaine_a_liste(nom_fichier.readline().strip('\n'))

        nom_fichier.close()

        self.tableau_mines = Tableau(self.dimension_rangee, self.dimension_colonne, nombre_mines=0)

        self.cadre = Frame(self)
        self.cadre.grid(padx=20, pady=20)

        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)
                bouton.bind('<ButtonRelease-1>', self.devoiler_case)
                bouton.bind('<ButtonRelease-3>', self.marquer_case)
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton

        self.compteur = Label(self.cadre)
        self.compteur.grid(row=self.tableau_mines.dimension_rangee + 2, column=self.tableau_mines.dimension_colonne + 2)
        self.compteur['text'] = "Nombre de tours : {}".format(self.nombre_de_tour)

        for bouton in self.dictionnaire_boutons.values():
            case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
            if (bouton.rangee_x, bouton.colonne_y) in position_mines:
                case.ajouter_mine()
                voisins = self.tableau_mines.obtenir_voisins(bouton.rangee_x, bouton.colonne_y)
                for i in voisins:
                    self.tableau_mines.dictionnaire_cases[i].ajouter_une_mine_voisine()
        for bouton in self.dictionnaire_boutons.values():
            case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
            if (bouton.rangee_x, bouton.colonne_y) in position_cases_devoilees:
                bouton['text'] = case.nombre_mines_voisines
                case.devoiler()
        for bouton in self.dictionnaire_boutons.values():
            case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
            if (bouton.rangee_x, bouton.colonne_y) in position_cases_marquees:
                BoutonCase.marquer(bouton)
                case.marquee()






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
            self.cadre.destroy()
            self.nouvelle_partie()
        else:
            self.quit()


    def demander_dimension(self):
        self.dimension_rangee = simpledialog.askinteger(title="Combien de rangée", prompt="", minvalue=1)
        if self.dimension_rangee == None:
            self.dimension_rangee=1
        self.dimension_colonne = simpledialog.askinteger(title="Combien de colonne", prompt="", minvalue=1)
        if self.dimension_colonne == None:
            self.dimension_colonne=1
        self.nombre_mines = simpledialog.askinteger(title="Combien de mines", prompt="", minvalue=0, maxvalue=self.dimension_rangee * self.dimension_colonne)
        if self.nombre_mines == None:
            self.nombre_mines=1


