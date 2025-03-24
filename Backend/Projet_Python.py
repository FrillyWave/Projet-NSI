
import copy
#Class pièce 

def coordonnees_to_case(liste):
    for i in range(len(liste)):
        nombre = 8 - liste[i][1]
        lettre = chr(65 + liste[i][0])
        liste[i] = lettre+str(nombre)
    return liste

class Piece:
    """
    Permet de représenter une Piece dans l'échequier
    Attributs :
        Nom : string
            Son nom tout simplement
        Position : string
            C'est une chaîne de caractère composé d'une lettre et d'un chiffre. Par exemple, B1, C5 ou E7.
        Type : string
            Une seule lettre : Q(Queen), B(Bishop), R(Rook), K(King), P(Pion), H(HorseMan)
        Couleur : boolean
            True blanc, False noir

    """

    def __init__(self, nom, position, type, couleur):
        self.Nom = nom
        self.Position = position
        self.Type = type
        self.Couleur = couleur 

    #==================================================
    #SETTER & GETTER
    #==================================================

    #Setter & Getter Nom

    def GetNom(self):
        return self.Nom

    def SetNom(self, new_nom):
        self.Nom = new_nom

    #Setter & Getter Position

    def GetPosition(self):
        return self.Position

    def SetPosition(self, new_position):
        self.Position = new_position

    #Setter & Getter Type
    
    def GetType(self):
        return self.Type

    def SetType(self, new_type):
        self.Type = new_type

    #Setter & Getter Couleur

    def GetCouleur(self):
        return self.Couleur

    def SetCouleur(self, new_couleur):
        self.Couleur = new_couleur

    def Translate_coordonnees(self):
        x = ord(self.Position[0]) - 65
        y = abs(int(self.Position[1]) - 8)
        return x,y 
    
    #==================================================
    #Mouvements pièces
    #==================================================

    

    def Mouvement_Possible(self, Echequier):
        piece_type = self.GetType()
        #Pion
        if piece_type == "P":
            liste_mouvements = self.Mouvement_Possible_Pion(Echequier)
        # King
        if piece_type == "K":
            liste_mouvements = self.Mouvement_Possible_King(Echequier)
        #Rook
        if piece_type == "R":
            liste_mouvements = self.Mouvement_Possible_Rook(Echequier)
        #Bishoop
        if piece_type == "B":
            liste_mouvements = self.Mouvement_Possible_Bishoop(Echequier)
        #Queen
        if piece_type == "Q":
            liste_mouvements = self.Mouvement_Possible_Queen(Echequier)
        #Horseman
        if piece_type == "H":
            liste_mouvements = self.Mouvement_Possible_Horseman(Echequier)


        return coordonnees_to_case(liste_mouvements)

    
    def Mouvement_Possible_Pion(self, Echequier):
        echequier = Echequier.GetContenue()  
        liste_mouvements = []
        piece_position = self.Translate_coordonnees()
        piece_color = self.GetCouleur()

        # avance 1 case classique 

        # Blanc
        if piece_color:
            if echequier[piece_position[1] - 1][piece_position[0]] == None:
                liste_mouvements.append((piece_position[0], piece_position[1] - 1))

        # Noir
        else:
            if echequier[piece_position[1] + 1][piece_position[0]] == None:
                liste_mouvements.append((piece_position[0], piece_position[1] + 1))

        # avance 2 cases au début

        # Blanc
        if piece_color:
            if piece_position[1] == 6 and (echequier[piece_position[1] - 1][piece_position[0]] == None and echequier[piece_position[1] - 2][piece_position[0]] == None):
                liste_mouvements.append((piece_position[0], piece_position[1] - 2))

        # Noir
        else:
            if piece_position[1] == 1 and (echequier[piece_position[1] + 1][piece_position[0]] == None and echequier[piece_position[1] + 2][piece_position[0]] == None):
                liste_mouvements.append((piece_position[0], piece_position[1] + 2))

        # manger en diagonale

        # Blanc
        if piece_color:
            # diagonale droite
            if piece_position[1] - 1 >= 0 and piece_position[0] + 1 <= 7:
                if echequier[piece_position[1] - 1][piece_position[0] + 1] != None:
                    if not(echequier[piece_position[1] - 1][piece_position[0] + 1].GetCouleur()):
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 1))
            # diagonale gauche
            if piece_position[1] - 1 >= 0 and piece_position[0] - 1 >= 0:
                if echequier[piece_position[1] - 1][piece_position[0] - 1] != None:
                    if not(echequier[piece_position[1] - 1][piece_position[0] - 1].GetCouleur()):
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 1))
        
        # Noir
        else:
            # diagonale droite
            if piece_position[1] + 1 <= 7 and piece_position[0] + 1 <= 7:
                if echequier[piece_position[1] + 1][piece_position[0] + 1] != None:
                    if echequier[piece_position[1] + 1][piece_position[0] + 1].GetCouleur():
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 1))
            # diagonale gauche
            if piece_position[1] + 1 <= 7 and piece_position[0] - 1 >= 0:
                if echequier[piece_position[1] + 1][piece_position[0] - 1] != None:
                    if echequier[piece_position[1] + 1][piece_position[0] - 1].GetCouleur():
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 1))

        return liste_mouvements

    def Mouvement_Possible_King(self, Echequier):
        echequier = Echequier.GetContenue()  
        liste_mouvements = []
        piece_position = self.Translate_coordonnees()
        piece_color = self.GetCouleur()

        # Blanc
        if piece_color:
            # Haut Gauche
            if piece_position[1] - 1 >= 0 and piece_position[0] - 1 >= 0:
                if echequier[piece_position[1] - 1][piece_position[0] - 1] == None:
                    liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 1))
                else:
                    if not(echequier[piece_position[1] - 1][piece_position[0] - 1].GetCouleur()):
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 1))
            # Haut 
            if piece_position[1] - 1 >= 0:
                if echequier[piece_position[1] - 1][piece_position[0]] == None:
                    liste_mouvements.append((piece_position[0], piece_position[1] - 1))
                else:
                    if not(echequier[piece_position[1] - 1][piece_position[0]].GetCouleur()):
                        liste_mouvements.append((piece_position[0], piece_position[1] - 1))
            # Haut droite
            if piece_position[1] - 1 >= 0 and piece_position[0] + 1 <= 7:
                if echequier[piece_position[1] - 1][piece_position[0] + 1] == None:
                    liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 1))
                else:
                    if not(echequier[piece_position[1] - 1][piece_position[0] + 1].GetCouleur()):
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 1))
            # Gauche
            if piece_position[0] - 1 >= 0:
                if echequier[piece_position[1]][piece_position[0] - 1] == None:
                    liste_mouvements.append((piece_position[0] - 1, piece_position[1]))
                else:
                    if not(echequier[piece_position[1]][piece_position[0] - 1].GetCouleur()):
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1]))
            # Bas Gauche
            if piece_position[0] - 1 >= 0 and piece_position[1] + 1 <= 7:
                if echequier[piece_position[1] + 1][piece_position[0] - 1] == None:
                    liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 1))
                else:
                    if not(echequier[piece_position[1] + 1][piece_position[0] - 1].GetCouleur()):
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 1))
            # Bas
            if piece_position[1] + 1 <= 7:
                if echequier[piece_position[1] + 1][piece_position[0]] == None:
                    liste_mouvements.append((piece_position[0], piece_position[1] + 1))
                else:
                    if not(echequier[piece_position[1] + 1][piece_position[0]].GetCouleur()):
                        liste_mouvements.append((piece_position[0], piece_position[1] + 1))
            # Bas Droite
            if piece_position[0] + 1 <= 7 and piece_position[1] + 1 <= 7:
                if echequier[piece_position[1] + 1][piece_position[0] + 1] == None:
                    liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 1))
                else:
                    if not(echequier[piece_position[1] + 1][piece_position[0] + 1].GetCouleur()):
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 1))
            # Droite 
            if piece_position[0] + 1 <= 7 :
                if echequier[piece_position[1]][piece_position[0] + 1] == None:
                    liste_mouvements.append((piece_position[0] + 1, piece_position[1]))
                else:
                    if not(echequier[piece_position[1]][piece_position[0] + 1].GetCouleur()):
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1]))

        # Noir
        else:
            # Haut Gauche
            if piece_position[1] - 1 >= 0 and piece_position[0] - 1 >= 0:
                if echequier[piece_position[1] - 1][piece_position[0] - 1] == None:
                    liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 1))
                else:
                    if echequier[piece_position[1] - 1][piece_position[0] - 1].GetCouleur():
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 1))
            # Haut 
            if piece_position[1] - 1 >= 0:
                if echequier[piece_position[1] - 1][piece_position[0]] == None:
                    liste_mouvements.append((piece_position[0], piece_position[1] - 1))
                else:
                    if echequier[piece_position[1] - 1][piece_position[0]].GetCouleur():
                        liste_mouvements.append((piece_position[0], piece_position[1] - 1))
            # Haut droite
            if piece_position[1] - 1 >= 0 and piece_position[0] + 1 <= 7:
                if echequier[piece_position[1] - 1][piece_position[0] + 1] == None:
                    liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 1))
                else:
                    if echequier[piece_position[1] - 1][piece_position[0] + 1].GetCouleur():
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 1))
            # Gauche
            if piece_position[0] - 1 >= 0:
                if echequier[piece_position[1]][piece_position[0] - 1] == None:
                    liste_mouvements.append((piece_position[0] - 1, piece_position[1]))
                else:
                    if echequier[piece_position[1]][piece_position[0] - 1].GetCouleur():
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1]))
            # Bas Gauche
            if piece_position[0] - 1 >= 0 and piece_position[1] + 1 <= 7:
                if echequier[piece_position[1] + 1][piece_position[0] - 1] == None:
                    liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 1))
                else:
                    if echequier[piece_position[1] + 1][piece_position[0] - 1].GetCouleur():
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 1))
            # Bas
            if piece_position[1] + 1 <= 7:
                if echequier[piece_position[1] + 1][piece_position[0]] == None:
                    liste_mouvements.append((piece_position[0], piece_position[1] + 1))
                else:
                    if echequier[piece_position[1] + 1][piece_position[0]].GetCouleur():
                        liste_mouvements.append((piece_position[0], piece_position[1] + 1))
            # Bas Droite
            if piece_position[0] + 1 <= 7 and piece_position[1] + 1 <= 7:
                if echequier[piece_position[1] + 1][piece_position[0] + 1] == None:
                    liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 1))
                else:
                    if echequier[piece_position[1] + 1][piece_position[0] + 1].GetCouleur():
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 1))
            # Droite 
            if piece_position[0] + 1 <= 7 :
                if echequier[piece_position[1]][piece_position[0] + 1] == None:
                    liste_mouvements.append((piece_position[0] + 1, piece_position[1]))
                else:
                    if echequier[piece_position[1]][piece_position[0] + 1].GetCouleur():
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1]))
        
        return liste_mouvements

    def Mouvement_Possible_Rook(self, Echequier):
        echequier = Echequier.GetContenue()  
        liste_mouvements = []
        piece_position = self.Translate_coordonnees()
        piece_color = self.GetCouleur()

        # Blanc
        if piece_color:
            for i in range(4):
                Path = True
                chain = 1
                if i == 0:
                    x = 0
                    y = 1
                elif i == 1:
                    x = 0
                    y = -1
                elif i == 2:
                    x = 1
                    y = 0
                else:
                    x = -1
                    y = 0
                while Path:
                    if (piece_position[1] + (y * chain) <= 7 and piece_position[1] + (y * chain) >= 0) and (piece_position[0] + (x * chain) <= 7 and piece_position[0] + (x * chain) >= 0):
                        if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)] == None:
                            if self.Movement_verif_echec((piece_position[0] + (x * chain), piece_position[1] + (y * chain)), Echequier):
                                liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                        else:
                            if not(echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)].GetCouleur()):
                                if self.Movement_verif_echec((piece_position[0] + (x * chain), piece_position[1] + (y * chain)), Echequier):
                                    liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                                    Path = False 
                            else:
                                Path = False
                    else:
                        Path = False
                    chain = chain + 1

        # Noir
        else:
            for i in range(4):
                Path = True
                chain = 1
                if i == 0:
                    x = 0
                    y = 1
                elif i == 1:
                    x = 0
                    y = -1
                elif i == 2:
                    x = 1
                    y = 0
                else:
                    x = -1
                    y = 0
                while Path:
                    if (piece_position[1] + (y * chain) <= 7 and piece_position[1] + (y * chain) >= 0) and (piece_position[0] + (x * chain) <= 7 and piece_position[0] + (x * chain) >= 0):
                        if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)] == None:
                            if self.Movement_verif_echec((piece_position[0] + (x * chain), piece_position[1] + (y * chain)), Echequier):
                                liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                        else:
                            if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)].GetCouleur():
                                if self.Movement_verif_echec((piece_position[0] + (x * chain), piece_position[1] + (y * chain)), Echequier):
                                    liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                                    Path = False 
                            else:
                                Path = False
                    else:
                        Path = False
                    chain = chain + 1

        return liste_mouvements

    def Mouvement_Possible_Bishoop(self, Echequier):
        echequier = Echequier.GetContenue()  
        liste_mouvements = []
        piece_position = self.Translate_coordonnees()
        piece_color = self.GetCouleur()

        # Blanc
        if piece_color:
            for i in range(4):
                Path = True
                chain = 1
                if i == 0:
                    x = 1
                    y = 1
                elif i == 1:
                    x = 1
                    y = -1
                elif i == 2:
                    x = -1
                    y = -1
                else:
                    x = -1
                    y = 1
                while Path:
                    if (piece_position[1] + (y * chain) <= 7 and piece_position[1] + (y * chain) >= 0) and (piece_position[0] + (x * chain) <= 7 and piece_position[0] + (x * chain) >= 0):
                        if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)] == None:
                            liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                        else:
                            if not(echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)].GetCouleur()):
                                liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                                Path = False 
                            else:
                                Path = False
                    else:
                        Path = False
                    chain = chain + 1

        # Noir
        else:
            for i in range(4):
                Path = True
                chain = 1
                if i == 0:
                    x = 1
                    y = 1
                elif i == 1:
                    x = 1
                    y = -1
                elif i == 2:
                    x = -1
                    y = -1
                else:
                    x = -1
                    y = 1
                while Path:
                    if (piece_position[1] + (y * chain) <= 7 and piece_position[1] + (y * chain) >= 0) and (piece_position[0] + (x * chain) <= 7 and piece_position[0] + (x * chain) >= 0):
                        if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)] == None:
                            liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                        else:
                            if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)].GetCouleur():
                                liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                                Path = False 
                            else:
                                Path = False
                    else:
                        Path = False
                    chain = chain + 1

        return liste_mouvements

    def Mouvement_Possible_Queen(self, Echequier):
        echequier = Echequier.GetContenue()  
        liste_mouvements = []
        piece_position = self.Translate_coordonnees()
        piece_color = self.GetCouleur()

        # Blanc
        if piece_color:
            #Bishoop
            for i in range(4):
                Path = True
                chain = 1
                if i == 0:
                    x = 1
                    y = 1
                elif i == 1:
                    x = 1
                    y = -1
                elif i == 2:
                    x = -1
                    y = -1
                else:
                    x = -1
                    y = 1
                while Path:
                    if (piece_position[1] + (y * chain) <= 7 and piece_position[1] + (y * chain) >= 0) and (piece_position[0] + (x * chain) <= 7 and piece_position[0] + (x * chain) >= 0):
                        if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)] == None:
                            liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                        else:
                            if not(echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)].GetCouleur()):
                                liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                                Path = False 
                            else:
                                Path = False
                    else:
                        Path = False
                    chain = chain + 1
            #rook        
            for i in range(4):
                Path = True
                chain = 1
                if i == 0:
                    x = 0
                    y = 1
                elif i == 1:
                    x = 0
                    y = -1
                elif i == 2:
                    x = 1
                    y = 0
                else:
                    x = -1
                    y = 0
                while Path:
                    if (piece_position[1] + (y * chain) <= 7 and piece_position[1] + (y * chain) >= 0) and (piece_position[0] + (x * chain) <= 7 and piece_position[0] + (x * chain) >= 0):
                        if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)] == None:
                            liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                        else:
                            if not(echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)].GetCouleur()):
                                liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                                Path = False 
                            else:
                                Path = False
                    else:
                        Path = False
                    chain = chain + 1

        # Noir
        else:
            #Bishoop
            for i in range(4):
                Path = True
                chain = 1
                if i == 0:
                    x = 1
                    y = 1
                elif i == 1:
                    x = 1
                    y = -1
                elif i == 2:
                    x = -1
                    y = -1
                else:
                    x = -1
                    y = 1
                while Path:
                    if (piece_position[1] + (y * chain) <= 7 and piece_position[1] + (y * chain) >= 0) and (piece_position[0] + (x * chain) <= 7 and piece_position[0] + (x * chain) >= 0):
                        if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)] == None:
                            liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                        else:
                            if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)].GetCouleur():
                                liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                                Path = False 
                            else:
                                Path = False
                    else:
                        Path = False
                    chain = chain + 1
            
            #rook
            for i in range(4):
                Path = True
                chain = 1
                if i == 0:
                    x = 0
                    y = 1
                elif i == 1:
                    x = 0
                    y = -1
                elif i == 2:
                    x = 1
                    y = 0
                else:
                    x = -1
                    y = 0
                while Path:
                    if (piece_position[1] + (y * chain) <= 7 and piece_position[1] + (y * chain) >= 0) and (piece_position[0] + (x * chain) <= 7 and piece_position[0] + (x * chain) >= 0):
                        if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)] == None:
                            liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                        else:
                            if echequier[piece_position[1] + (y * chain)][piece_position[0] + (x * chain)].GetCouleur():
                                liste_mouvements.append((piece_position[0] + (x * chain), piece_position[1] + (y * chain)))
                                Path = False 
                            else:
                                Path = False
                    else:
                        Path = False
                    chain = chain + 1

        return liste_mouvements
    
    def Mouvement_Possible_Horseman(self, Echequier):
        echequier = Echequier.GetContenue()  
        liste_mouvements = []
        piece_position = self.Translate_coordonnees()
        piece_color = self.GetCouleur()

        # Blanc
        if piece_color:
            # Haut
            if piece_position[1] - 2 >= 0 :
                # Droite
                if piece_position[0] + 1 <= 7 :
                    if echequier[piece_position[1] - 2][piece_position[0] + 1] == None:
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 2))
                    else:
                        if not(echequier[piece_position[1] - 2][piece_position[0] + 1].GetCouleur()):
                            liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 2))
                
                # Gauche
                if piece_position[0] - 1 >= 0 :
                    if echequier[piece_position[1] - 2][piece_position[0] - 1] == None:
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 2))
                    else:
                        if not(echequier[piece_position[1] - 2][piece_position[0] - 1].GetCouleur()):
                            liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 2))

            # Bas
            if piece_position[1] + 2 <= 7 :
                # Droite
                if piece_position[0] + 1 <= 7 :
                    if echequier[piece_position[1] + 2][piece_position[0] + 1] == None:
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 2))
                    else:
                        if not(echequier[piece_position[1] + 2][piece_position[0] + 1].GetCouleur()):
                            liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 2))
                
                # Gauche
                if piece_position[0] - 1 >= 0 :
                    if echequier[piece_position[1] + 2][piece_position[0] - 1] == None:
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 2))
                    else:
                        if not(echequier[piece_position[1] + 2][piece_position[0] - 1].GetCouleur()):
                            liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 2))

            # Gauche
            if piece_position[0] - 2 >= 0 :
                # bas
                if piece_position[1] + 1 <= 7 :
                    if echequier[piece_position[1] + 1][piece_position[0] - 2] == None:
                        liste_mouvements.append((piece_position[0] - 2, piece_position[1] + 1))
                    else:
                        if not(echequier[piece_position[1] + 1][piece_position[0] - 2].GetCouleur()):
                            liste_mouvements.append((piece_position[0] - 2, piece_position[1] + 1))
                
                # haut
                if piece_position[1] - 1 >= 0 :
                    if echequier[piece_position[1] - 1][piece_position[0] - 2] == None:
                        liste_mouvements.append((piece_position[0] - 2, piece_position[1] - 1))
                    else:
                        if not(echequier[piece_position[1] - 1][piece_position[0] - 2].GetCouleur()):
                            liste_mouvements.append((piece_position[0] - 2, piece_position[1] - 1))

            # Droite
            if piece_position[0] + 2 <= 7 :
                # bas
                if piece_position[1] + 1 <= 7 :
                    if echequier[piece_position[1] + 1][piece_position[0] + 2] == None:
                        liste_mouvements.append((piece_position[0] + 2, piece_position[1] + 1))
                    else:
                        if not(echequier[piece_position[1] + 1][piece_position[0] + 2].GetCouleur()):
                            liste_mouvements.append((piece_position[0] + 2, piece_position[1] + 1))
                
                # haut
                if piece_position[1] - 1 >= 0 :
                    if echequier[piece_position[1] - 1][piece_position[0] + 2] == None:
                        liste_mouvements.append((piece_position[0] + 2, piece_position[1] - 1))
                    else:
                        if not(echequier[piece_position[1] - 1][piece_position[0] + 2].GetCouleur()):
                            liste_mouvements.append((piece_position[0] + 2, piece_position[1] - 1))
                    
        # Noir
        else:
            # Haut
            if piece_position[1] - 2 >= 0 :
                # Droite
                if piece_position[0] + 1 <= 7 :
                    if echequier[piece_position[1] - 2][piece_position[0] + 1] == None:
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 2))
                    else:
                        if echequier[piece_position[1] - 2][piece_position[0] + 1].GetCouleur():
                            liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 2))
                
                # Gauche
                if piece_position[0] - 1 >= 0 :
                    if echequier[piece_position[1] - 2][piece_position[0] - 1] == None:
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 2))
                    else:
                        if echequier[piece_position[1] - 2][piece_position[0] - 1].GetCouleur():
                            liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 2))

            # Bas
            if piece_position[1] + 2 <= 7 :
                # Droite
                if piece_position[0] + 1 <= 7 :
                    if echequier[piece_position[1] + 2][piece_position[0] + 1] == None:
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 2))
                    else:
                        if echequier[piece_position[1] + 2][piece_position[0] + 1].GetCouleur():
                            liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 2))
                
                # Gauche
                if piece_position[0] - 1 >= 0 :
                    if echequier[piece_position[1] + 2][piece_position[0] - 1] == None:
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 2))
                    else:
                        if echequier[piece_position[1] + 2][piece_position[0] - 1].GetCouleur():
                            liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 2))

            # gauche
            if piece_position[0] - 2 >= 0 :
                # bas
                if piece_position[1] + 1 <= 7 :
                    if echequier[piece_position[1] + 1][piece_position[0] - 2] == None:
                        liste_mouvements.append((piece_position[0] - 2, piece_position[1] + 1))
                    else:
                        if echequier[piece_position[1] + 1][piece_position[0] - 2].GetCouleur():
                            liste_mouvements.append((piece_position[0] - 2, piece_position[1] + 1))
                
                # haut
                if piece_position[1] - 1 >= 0 :
                    if echequier[piece_position[1] - 1][piece_position[0] - 2] == None:
                        liste_mouvements.append((piece_position[0] - 2, piece_position[1] - 1))
                    else:
                        if echequier[piece_position[1] - 1][piece_position[0] - 2].GetCouleur():
                            liste_mouvements.append((piece_position[0] - 2, piece_position[1] - 1 ))

            # droite
            if piece_position[0] + 2 <= 7 :
                # bas
                if piece_position[1] + 1 <= 7 :
                    if echequier[piece_position[1] + 1][piece_position[0] + 2] == None:
                        liste_mouvements.append((piece_position[0] + 2, piece_position[1] + 1))
                    else:
                        if echequier[piece_position[1] + 1][piece_position[0] + 2].GetCouleur():
                            liste_mouvements.append((piece_position[0] + 2, piece_position[1] + 1))
                
                # haut
                if piece_position[1] - 1 >= 0 :
                    if echequier[piece_position[1] - 1][piece_position[0] + 2] == None:
                        liste_mouvements.append((piece_position[0] + 2, piece_position[1] - 1))
                    else:
                        if echequier[piece_position[1] - 1][piece_position[0] + 2].GetCouleur():
                            liste_mouvements.append((piece_position[0] + 2, piece_position[1] - 1))

        return liste_mouvements

    def Move(self, coordonnees, Echequier):
        echequier = Echequier.GetContenue()
        Liste_mouvement_possible = self.Mouvement_Possible(Echequier)
        if coordonnees in Liste_mouvement_possible:
            echequier[self.Translate_coordonnees()[1]][self.Translate_coordonnees()[0]] = None
            self.SetPosition(coordonnees)
            Echequier.Ajouter_Piece(self)
        else:
            return "Non"

    def Movement_verif_echec(self, coordonnees, Echequier):
        echequier = Echequier.GetContenue()
        Back_up_case = echequier[coordonnees[1]][coordonnees[0]]
        print(Back_up_case)
        Back_up_piece_coordonnees = self.GetPosition()
        print(Back_up_piece_coordonnees)
        print(coordonnees)

        #Blanc
        if self.GetCouleur():
            echequier[coordonnees[1]][coordonnees[0]] = None
            self.SetPosition(coordonnees_to_case([coordonnees])[0])
            Echequier.Ajouter_Piece(self)
            if Echequier.Echec_blanc():
                return True
            else:
                self.SetPosition(Back_up_piece_coordonnees)
                echequier[coordonnees[1]][coordonnees[0]] = Back_up_case
                Echequier.Ajouter_Piece(self)
                return False

        #noir
        else:
            echequier[coordonnees[1]][coordonnees[0]] = None
            self.SetPosition(coordonnees_to_case([coordonnees])[0])
            Echequier.Ajouter_Piece(self)
            if Echequier.Echec_noir():
                return True
            else:
                self.SetPosition(Back_up_piece_coordonnees)
                echequier[coordonnees[1]][coordonnees[0]] = Back_up_case
                Echequier.Ajouter_Piece(self)
                return False

    #==================================================
    #
    #==================================================
                


    def __repr__(self):
        return f"Piece : \n Nom : {self.Nom} \n Position : {self.Position} \n Type : {self.Type} \n Couleur : {self.Couleur}"

#Class échequier 

class Echequier:
    """
    Permet de représenter un échequier, il est composé d'objet de l'instance Piece.
    Attributs :
        Contenue : list
            Une liste en 2D de case vide ou d'objet de la classe Piece 
    """

    def __init__(self):
        self.Contenue = [[None for x in range(8)] for y in range(8)]

    #Setter & Getter Contenue

    def GetContenue(self):
        return self.Contenue

    def SetContenue(self, new_contenue):
        self.Contenue = new_contenue

    def Affichage_provisoire(self):
        echequier = self.GetContenue()
        Console = "    A   B   C   D   E   F   G   H  \n"
        for y in range(8):
            Console = Console + ' '+ str(8-y) + ' '
            for x in range(8):
                if echequier[y][x] != None:
                    Console = Console + echequier[y][x].Nom + " "
                else:
                    Console = Console + "XXX "
            Console = Console + "\n"
        return Console

    def Ajouter_Piece(self, piece):
        echequier = self.GetContenue()
        x = ord(piece.Position[0]) - 65
        y = abs(int(piece.Position[1]) - 8)
        echequier[y][x] = piece
        self.Contenue = echequier

    def All_move(self):
        echequier = self.GetContenue()
        liste_mouvements_blanc = []
        liste_mouvements_noir = []
        liste_mouvements_piece = []
        for i in range(8):
            for j in range(8):
                if echequier[i][j] != None:
                    piece = echequier[i][j]
                    liste_mouvements_piece = piece.Mouvement_Possible(self)
                    if piece.GetCouleur():
                        for u in range(len(liste_mouvements_piece)):
                            liste_mouvements_blanc.append(liste_mouvements_piece[u])
                    else:
                        for u in range(len(liste_mouvements_piece)):
                            liste_mouvements_noir.append(liste_mouvements_piece[u])

        return (liste_mouvements_blanc, liste_mouvements_noir)

    def Echec_blanc(self):
        echequier = self.GetContenue()
        #trouver le roi
        case_king = K1.GetPosition()
        #verif que le roi est safe
        All_move = self.All_move()[1]
        for i in range(len(All_move)):
            if All_move[i] == case_king:
                return True
        return False

    def Echec_noir(self):
        echequier = self.GetContenue()
        #trouver le roi
        case_king = k1.GetPosition()
        #verif que le roi est safe
        All_move = self.All_move()[0]
        for i in range(len(All_move)):
            if All_move[i] == case_king:
                return True
        return False

    def __repr__(self):
        return f"Echequier : {self.Contenue}"

#=============================================================================
#ZONE TEST
#=============================================================================

Zone_test = Echequier()


P1 = Piece(" P1", "C2", "P", True)
P2 = Piece(" P2", "D2", "P", True)
p1 = Piece(" p1", "D3", "P", False)
R1 = Piece(" R1", "F3", "R", True)
b1 = Piece(" b1", "E4", "B", False)
Q1 = Piece(" Q1", "C4", "Q", True)
h1 = Piece(" h1", "D6", "H", False)
K1 = Piece(" K1", "A3", "K", True)
k1 = Piece(" k1", "C8", "K", False)
r1 = Piece(" r1", "C6", "R", False)


Zone_test.Ajouter_Piece(P1)
Zone_test.Ajouter_Piece(P2)
Zone_test.Ajouter_Piece(p1)
Zone_test.Ajouter_Piece(R1)
Zone_test.Ajouter_Piece(b1)
Zone_test.Ajouter_Piece(Q1)
Zone_test.Ajouter_Piece(h1)
Zone_test.Ajouter_Piece(K1)
Zone_test.Ajouter_Piece(k1)
Zone_test.Ajouter_Piece(r1)

print(Zone_test.Affichage_provisoire())

#print("P1 : ", P1.Mouvement_Possible(Zone_test))
#print("P2 : ", P2.Mouvement_Possible(Zone_test))
#print("p1 : ", p1.Mouvement_Possible(Zone_test))
#print("R1 : ", R1.Mouvement_Possible(Zone_test))
#print("b1 : ", b1.Mouvement_Possible(Zone_test))
#print("Q1 : ", Q1.Mouvement_Possible(Zone_test))
#print("h1 : ", h1.Mouvement_Possible(Zone_test))
#print("K1 : ", K1.Mouvement_Possible(Zone_test))
print("r1 : ", r1.Mouvement_Possible(Zone_test))

#print("All Move : ", Zone_test.All_move())

#print("Blanc en échec ? : ", Zone_test.Echec_blanc())
#print("Noir en échec ? : ", Zone_test.Echec_noir())

#P1.Move("D3", Zone_test)

#print(Zone_test.Affichage_provisoire())
#=============================================================================
#
#=============================================================================
