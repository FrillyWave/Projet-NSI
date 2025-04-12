import copy
#Class pièce 

def coordonnees_to_case(liste):
    for i in range(len(liste)):
        nombre = 8 - liste[i][1]
        lettre = chr(65 + liste[i][0])
        liste[i] = lettre+str(nombre)
    return liste

def Translate_coordonnees(coordonnees):
        x = ord(coordonnees[0]) - 65
        y = abs(int(coordonnees[1]) - 8)
        return x,y 

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
        Deplacement : (int, boolean)
            Sert à savoir si une pièce à déja bougée ou non et si elle à avancer deux 2 cases pour un pion. Utile pour les déplacements spéciaux.

    """

    def __init__(self, nom, position, type, couleur):
        self.Nom = nom
        self.Position = position
        self.Type = type
        self.Couleur = couleur 
        self.Deplacement = (0, False)

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

    #Setter & Getter Deplacement

    def GetDeplacement(self):
        return self.Deplacement

    def SetDeplacement(self, new_Deplacement):
        self.Deplacement = new_Deplacement

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

        # En passant 

        # Blanc
        if piece_color:
            # diagonale droite
            if piece_position[1] - 1 >= 0 and piece_position[0] + 1 <= 7:
                if echequier[piece_position[1]][piece_position[0] + 1] != None:
                    if echequier[piece_position[1]][piece_position[0] + 1].GetDeplacement()[0] == 1 and echequier[piece_position[1]][piece_position[0] + 1].GetDeplacement()[1]:
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 1))
            # diagonale gauche
            if piece_position[1] - 1 >= 0 and piece_position[0] - 1 >= 0:
                if echequier[piece_position[1]][piece_position[0] - 1] != None:
                    if echequier[piece_position[1]][piece_position[0] - 1].GetDeplacement()[0] == 1 and echequier[piece_position[1]][piece_position[0] - 1].GetDeplacement()[1]:
                        liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 1))

        # Noir
        else:
            # diagonale droite
            if piece_position[1] + 1 <= 7 and piece_position[0] + 1 <= 7:
                if echequier[piece_position[1]][piece_position[0] + 1] != None:
                    if echequier[piece_position[1]][piece_position[0] + 1].GetDeplacement()[0] == 1 and echequier[piece_position[1]][piece_position[0] + 1].GetDeplacement()[1]:
                        liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 1))
            # diagonale gauche
            if piece_position[1] + 1 <= 7 and piece_position[0] - 1 >= 0:
                if echequier[piece_position[1]][piece_position[0] - 1] != None:
                    if echequier[piece_position[1]][piece_position[0] - 1].GetDeplacement()[0] == 1 and echequier[piece_position[1]][piece_position[0] - 1].GetDeplacement()[1]:
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

            # petit rook 
            if K1.GetDeplacement()[0] == 0 and R2.GetDeplacement()[0] == 0:
                if echequier[7][5] == None and echequier[7][6] == None:
                    if echequier[7][7] == R2:
                        liste_mouvements.append((6,7))
                    

            # grand rock
            if K1.GetDeplacement()[0] == 0 and R1.GetDeplacement()[0] == 0:
                if echequier[7][1] == None and echequier[7][2] == None and echequier[7][3] == None and echequier[7][0] != None:
                    if echequier[7][0] == R1:
                        liste_mouvements.append((1,7))

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

            # petit rook 
            if k1.GetDeplacement()[0] == 0 and r2.GetDeplacement()[0] == 0:
                if echequier[0][5] == None and echequier[0][6] == None and echequier[0][7] != None:
                    if echequier[0][7] == r2:
                        liste_mouvements.append((6,0))

            # grand rock
            if k1.GetDeplacement()[0] == 0 and r1.GetDeplacement()[0] == 0:
                if echequier[0][1] == None and echequier[0][2] == None and echequier[0][3] == None and echequier[0][0] != None:
                    if echequier[0][0] == r1:
                        liste_mouvements.append((1,0))
        
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

        #Grand et petit rock
        if self.GetType() == 'K':
            #Blanc 
            if self.GetCouleur():
                #petit rock
                if coordonnees == "G1" and  "G1" in Liste_mouvement_possible:
                    if K1.GetDeplacement()[0] == 0 and R2.GetDeplacement()[0] == 0:
                        Liste_mouvement_possible.remove("G1")
                        if K1.Movement_verif_echec((6,7), Echequier) and K1.Movement_verif_echec((5,7), Echequier) and not(Echequier.Echec_blanc()):
                            echequier[7][4] = None
                            K1.Position = "G1"
                            Echequier.Ajouter_Piece(K1)
                            Echequier.SetContenue(echequier)
                            K1.SetDeplacement((K1.GetDeplacement()[0]+1 ,K1.GetDeplacement()[1]))

                            echequier[7][7] = None
                            R2.Position = "F1"
                            Echequier.Ajouter_Piece(R2)
                            Echequier.SetContenue(echequier)
                            R2.SetDeplacement((R2.GetDeplacement()[0]+1 ,R2.GetDeplacement()[1]))
                #grand rock
                if coordonnees == "B1" and  "B1" in Liste_mouvement_possible:
                    if K1.GetDeplacement()[0] == 0 and R1.GetDeplacement()[0] == 0:
                        Liste_mouvement_possible.remove("B1")
                        if K1.Movement_verif_echec((1,7), Echequier) and K1.Movement_verif_echec((2,7), Echequier) and K1.Movement_verif_echec((3,7), Echequier) and not(Echequier.Echec_blanc()):
                            echequier[7][4] = None
                            K1.Position = "B1"
                            Echequier.Ajouter_Piece(K1)
                            Echequier.SetContenue(echequier)
                            K1.SetDeplacement((K1.GetDeplacement()[0]+1 ,K1.GetDeplacement()[1]))

                            echequier[7][0] = None
                            R1.Position = "C1"
                            Echequier.Ajouter_Piece(R1)
                            Echequier.SetContenue(echequier)
                            R1.SetDeplacement((R1.GetDeplacement()[0]+1 ,R1.GetDeplacement()[1]))
                                 
            else:
                #petit rock
                if coordonnees == "G8" and  "G8" in Liste_mouvement_possible:
                    if k1.GetDeplacement()[0] == 0 and r2.GetDeplacement()[0] == 0:
                        Liste_mouvement_possible.remove("G8")
                        if k1.Movement_verif_echec((6,0), Echequier) and k1.Movement_verif_echec((5,0), Echequier) and not(Echequier.Echec_noir()):
                            echequier[0][4] = None
                            k1.Position = "G8"
                            Echequier.Ajouter_Piece(k1)
                            Echequier.SetContenue(echequier)
                            k1.SetDeplacement((k1.GetDeplacement()[0]+1 ,k1.GetDeplacement()[1]))

                            echequier[0][7] = None
                            r2.Position = "F8"
                            Echequier.Ajouter_Piece(r2)
                            Echequier.SetContenue(echequier)
                            r2.SetDeplacement((r2.GetDeplacement()[0]+1 ,r2.GetDeplacement()[1]))
                #grand rock
                if coordonnees == "B8"  and  "B8" in Liste_mouvement_possible:
                    if k1.GetDeplacement()[0] == 0 and r1.GetDeplacement()[0] == 0:
                        Liste_mouvement_possible.remove("B8")
                        if k1.Movement_verif_echec((1,0), Echequier) and k1.Movement_verif_echec((2,0), Echequier) and k1.Movement_verif_echec((3,0), Echequier) and not(Echequier.Echec_noir()):
                            echequier[0][4] = None
                            k1.Position = "B8"
                            Echequier.Ajouter_Piece(k1)
                            Echequier.SetContenue(echequier)
                            k1.SetDeplacement((k1.GetDeplacement()[0]+1 ,k1.GetDeplacement()[1]))

                            echequier[0][0] = None
                            r1.Position = "C8"
                            Echequier.Ajouter_Piece(r1)
                            Echequier.SetContenue(echequier)
                            r1.SetDeplacement((r1.GetDeplacement()[0]+1 ,r1.GetDeplacement()[1]))
        ancienne_coordonnees = (self.Translate_coordonnees()[0], self.Translate_coordonnees()[1])
        if coordonnees in Liste_mouvement_possible:
            if self.Movement_verif_echec(Translate_coordonnees(coordonnees), Echequier):
                echequier[ancienne_coordonnees[1]][ancienne_coordonnees[0]] = None
                self.Position = coordonnees
                Echequier.Ajouter_Piece(self)
                Echequier.SetContenue(echequier)

                
                
                #pion fin de ligne + prépa en passant + en passant
                if self.GetType() == 'P':
                    #blanc
                    if self.GetCouleur():
                        #prépa en passant 
                        if self.Translate_coordonnees()[1] == 4 and self.GetDeplacement()[0] == 0:
                            self.SetDeplacement((self.GetDeplacement()[0] ,True))
                        #pion fin de ligne
                        if self.Translate_coordonnees()[1] == 0:
                            change = str(input("En quoi veux tu transformer ton pion ? (H, Q, B, R)"))
                            self.SetType(change)
                            self.SetNom(change+"  ")
                        #en passant
                        if echequier[self.Translate_coordonnees()[1] + 1][self.Translate_coordonnees()[0]] != None:
                            if echequier[self.Translate_coordonnees()[1] + 1][self.Translate_coordonnees()[0]].GetDeplacement()[0] == 1 and echequier[self.Translate_coordonnees()[1] + 1][self.Translate_coordonnees()[0]].GetDeplacement()[1]:
                                echequier[self.Translate_coordonnees()[1] + 1][self.Translate_coordonnees()[0]] = None
                                Echequier.SetContenue(echequier)
                    #noir
                    else:
                        #prépa en passant 
                        if self.Translate_coordonnees()[1] == 3 and self.GetDeplacement()[0] == 0:
                            self.SetDeplacement((self.GetDeplacement()[0] ,True))
                        #pion fin de ligne
                        if self.Translate_coordonnees()[1] == 7:
                            change = str(input("En quoi veux tu transformer ton pion ? (H, Q, B, R)"))
                            self.SetType(change)
                            self.SetNom(change.lower()+"  ")
                        #en passant
                        if echequier[self.Translate_coordonnees()[1] - 1][self.Translate_coordonnees()[0]] != None:
                            if echequier[self.Translate_coordonnees()[1] - 1][self.Translate_coordonnees()[0]].GetDeplacement()[0] == 1 and echequier[self.Translate_coordonnees()[1] - 1][self.Translate_coordonnees()[0]].GetDeplacement()[1]:
                                echequier[self.Translate_coordonnees()[1] - 1][self.Translate_coordonnees()[0]] = None
                                Echequier.SetContenue(echequier)
                    self.SetDeplacement((self.GetDeplacement()[0]+1 ,self.GetDeplacement()[1]))
                return True
        return False

    def Movement_verif_echec(self, coordonnees, Echequier):
        #PB échec mat rock
        if self.GetType() == "K":
            #Blanc
            if self.GetCouleur():
                if Echequier.Echec_blanc():
                    if K1.GetDeplacement()[0] == 0 and ((coordonnees == (1,7)) or (coordonnees == (6,7))):
                        return False

            #Noir
            else:
                if Echequier.Echec_noir():
                    if k1.GetDeplacement()[0] == 0 and ((coordonnees == (1,0)) or (coordonnees == (6,0))):
                        return False
        echequier = Echequier.GetContenue()
        Back_up_case = echequier[coordonnees[1]][coordonnees[0]]
        Back_up_piece_coordonnees = self.GetPosition()
        #Blanc
        if self.GetCouleur():
            echequier[coordonnees[1]][coordonnees[0]] = None
            self.SetPosition(coordonnees_to_case([coordonnees])[0])
            Echequier.Ajouter_Piece(self)
            if not(Echequier.Echec_blanc()):
                self.SetPosition(Back_up_piece_coordonnees)
                echequier[coordonnees[1]][coordonnees[0]] = Back_up_case
                Echequier.Ajouter_Piece(self)
                return True
            else:
                self.SetPosition(Back_up_piece_coordonnees)
                echequier[coordonnees[1]][coordonnees[0]] = Back_up_case
                Echequier.Ajouter_Piece(self)
                return False

        #noir
        else:
            echequier[self.Translate_coordonnees()[1]][self.Translate_coordonnees()[0]] = None
            self.SetPosition(coordonnees_to_case([coordonnees])[0])
            Echequier.SetContenue(echequier)
            Echequier.Ajouter_Piece(self)
            if not(Echequier.Echec_noir()):
                self.SetPosition(Back_up_piece_coordonnees)
                echequier[coordonnees[1]][coordonnees[0]] = Back_up_case
                Echequier.Ajouter_Piece(self)
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
        return f"{self.Nom}"

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
    def EchecMat_noir(self):
        echequier = self.GetContenue()
        if self.Echec_noir():
            Liste_piece = []
            for y in range(8):
                for x in range(8):
                    if echequier[y][x] != None:
                        if not(echequier[y][x].GetCouleur()):
                            Liste_piece.append(echequier[y][x])
            for i in range(len(Liste_piece)):
                Liste_piece_mouvement = Liste_piece[i].Mouvement_Possible(self)
                for u in range(len(Liste_piece_mouvement)):
                    if Liste_piece[i].Movement_verif_echec(Translate_coordonnees(Liste_piece_mouvement[u]), self):
                        print(Liste_piece[i], Liste_piece_mouvement[u])
                        return False
            return True
        else:
            return False
    

    def EchecMat_blanc(self):
        echequier = self.GetContenue()
        if self.Echec_blanc():
            Liste_piece = []
            for y in range(8):
                for x in range(8):
                    if echequier[y][x] != None:
                        if echequier[y][x].GetCouleur():
                            Liste_piece.append(echequier[y][x])
            for i in range(len(Liste_piece)):
                Liste_piece_mouvement = Liste_piece[i].Mouvement_Possible(self)
                for u in range(len(Liste_piece_mouvement)):
                    if Liste_piece[i].Movement_verif_echec(Translate_coordonnees(Liste_piece_mouvement[u]), self):
                        return False
            return True
        else:
            return False

    def Nulle_evidente(self):
        echequier = self.GetContenue()

        #pat
        Pat = True
        #création liste piece blanc
        Liste_piece = []
        for y in range(8):
            for x in range(8):
                if echequier[y][x] != None:
                    if echequier[y][x].GetCouleur():
                        Liste_piece.append(echequier[y][x])
        #test pat blanc
        for i in range(len(Liste_piece)):
            Liste_piece_mouvement = Liste_piece[i].Mouvement_Possible(self)
            for u in range(len(Liste_piece_mouvement)):
                if Liste_piece[i].Movement_verif_echec(Translate_coordonnees(Liste_piece_mouvement[u]), self):
                    Pat = False

        if Pat:
            return True
        Pat = True
        #création liste piece noir
        Liste_piece = []
        for y in range(8):
            for x in range(8):
                if echequier[y][x] != None:
                    if not(echequier[y][x].GetCouleur()):
                        Liste_piece.append(echequier[y][x])
        #test pat noir
        for i in range(len(Liste_piece)):
            Liste_piece_mouvement = Liste_piece[i].Mouvement_Possible(self)
            for u in range(len(Liste_piece_mouvement)):
                if Liste_piece[i].Movement_verif_echec(Translate_coordonnees(Liste_piece_mouvement[u]), self):
                    Pat = False
        if Pat:
            return True
                    
        #obtention listes piece noir & blanc
        Liste_piece_blanc = []
        Liste_piece_noir = []
        for y in range(8):
            for x in range(8):
                if echequier[y][x] != None:
                    if echequier[y][x].GetCouleur():
                        Liste_piece_blanc.append(echequier[y][x].GetType())
                    else:
                        Liste_piece_noir.append(echequier[y][x].GetType())

        Liste_piece_noir.sort()
        Liste_piece_blanc.sort()
        Combinaison_perdante = [["K"],["B", "K"],["H", "K"]]
        if Liste_piece_blanc in Combinaison_perdante and Liste_piece_noir in Combinaison_perdante:
            return True
        else:
            return False

    def Avantage(self):
        Value_Noir = 0
        Value_Blanc = 0
        echequier = self.GetContenue()
        for y in range(8):
            for x in range(8):
                if echequier[y][x] != None:
                    piece_type = echequier[y][x].GetType()
                    if echequier[y][x].GetCouleur():
                        #Pion
                        if piece_type == "P":
                            Value_Blanc = Value_Blanc + 1
                        #Rook
                        if piece_type == "R":
                            Value_Blanc = Value_Blanc + 5
                        #Bishoop
                        if piece_type == "B":
                            Value_Blanc = Value_Blanc + 3
                        #Queen
                        if piece_type == "Q":
                            Value_Blanc = Value_Blanc + 9
                        #Horseman
                        if piece_type == "H":
                            Value_Blanc = Value_Blanc + 3
                    else:
                        #Pion
                        if piece_type == "P":
                            Value_Noir = Value_Noir + 1
                        #Rook
                        if piece_type == "R":
                            Value_Noir = Value_Noir + 5
                        #Bishoop
                        if piece_type == "B":
                            Value_Noir = Value_Noir + 3
                        #Queen
                        if piece_type == "Q":
                            Value_Noir = Value_Noir + 9
                        #Horseman
                        if piece_type == "H":
                            Value_Noir = Value_Noir + 3
        return Value_Blanc - Value_Noir

    def __repr__(self):
        return f"Echequier : {self.Contenue}"

def Best_Move(E, Couleur):
    echequier = E.GetContenue()
    Back_up = echequier
    Liste = []
    for y in range(8):
        for x in range(8):
            if echequier[y][x] != None:
                if echequier[y][x].GetCouleur() == Couleur:
                    ALL = echequier[y][x].Mouvement_Possible(E)
                    for i in range(len(ALL)):  
                        echequier[y][x].Move(ALL[i],E)
                        Liste.append(( E.Avantage()))

                    


def Bot(E, Couleur):
    pass



def Main():
    Mode = input("PVP ou BOT ?")
    echequier = E.GetContenue()
    Turn = True
    loop = True
    while not(E.EchecMat_blanc()) and not(E.EchecMat_noir()) and not(E.Nulle_evidente()):
        print(E.Affichage_provisoire())
        print(E.Avantage())
        loop = True
        if Turn:
            print("C'est aux Blancs de jouer !")
            while loop:
                loop = False
                CO_Piece = input("Quelle pièce voulez vous déplacer (Exemple : 'A3') ?")
                CO_Piece = Translate_coordonnees(CO_Piece)
                if echequier[CO_Piece[1]][CO_Piece[0]] != None:
                    if echequier[CO_Piece[1]][CO_Piece[0]].GetCouleur():
                        Deplacement_Piece = input("Ou voulez vous la déplacer (Exemple : 'B7') ?")
                        if echequier[CO_Piece[1]][CO_Piece[0]].Move(Deplacement_Piece, E):
                            Turn = not(Turn)
                        else:
                            loop = True
                            print("Impossible")
                    else:
                        loop = True
                        print("Impossible")
                else:
                    loop = True
                    print("Impossible")
        else:
            print("C'est aux Noirs de jouer !")
            while loop:
                loop = False
                CO_Piece = input("Quelle pièce voulez vous déplacer (Exemple : 'A3') ?")
                CO_Piece = Translate_coordonnees(CO_Piece)
                if echequier[CO_Piece[1]][CO_Piece[0]] != None:
                    if not(echequier[CO_Piece[1]][CO_Piece[0]].GetCouleur()):
                        Deplacement_Piece = input("Ou voulez vous la déplacer (Exemple : 'B7') ?")
                        if echequier[CO_Piece[1]][CO_Piece[0]].Move(Deplacement_Piece, E):
                            Turn = not(Turn)

                        else:
                            loop = True
                            print("Impossible")
                    else:
                        loop = True
                        print("Impossible")
                else:
                    loop = True
                    print("Impossible")
    print(E.Affichage_provisoire())
    if E.Nulle_evidente():
        return "Egalité"
    if Turn :
        return "Victoire des Noirs"
    else:
        return "Victoire des Blancs"
                    





#=============================================================================
#ZONE TEST
#=============================================================================
#Set up échequier initiale 
E = Echequier()
echequier = E.GetContenue()
#Blanc 
#Créer pièces
#Première ligne
P1 = Piece(" P1", "A2", "P", True)
P2 = Piece(" P2", "B2", "P", True)
P3 = Piece(" P3", "C2", "P", True)
P4 = Piece(" P4", "D2", "P", True)
P5 = Piece(" P5", "E2", "P", True)
P6 = Piece(" P6", "F2", "P", True)
P7 = Piece(" P7", "G2", "P", True)
P8 = Piece(" P8", "H2", "P", True)
#Deuxième ligne
R1 = Piece(" R1", "A1", "R", True)
H1 = Piece(" H1", "B1", "H", True)
B1 = Piece(" B1", "C1", "B", True)
Q1 = Piece(" Q1", "D1", "Q", True)
K1 = Piece(" K1", "E1", "K", True)
B2 = Piece(" B2", "F1", "B", True)
H2 = Piece(" H2", "G1", "H", True)
R2 = Piece(" R2", "H1", "R", True)
#Ajouter pièces à l'échequier
#Première ligne
E.Ajouter_Piece(P1)
E.Ajouter_Piece(P2)
E.Ajouter_Piece(P3)
E.Ajouter_Piece(P4)
E.Ajouter_Piece(P5)
E.Ajouter_Piece(P6)
E.Ajouter_Piece(P7)
E.Ajouter_Piece(P8)
#Deuxième ligne
E.Ajouter_Piece(R1)
E.Ajouter_Piece(H1)
E.Ajouter_Piece(B1)
E.Ajouter_Piece(Q1)
E.Ajouter_Piece(K1)
E.Ajouter_Piece(B2)
E.Ajouter_Piece(H2)
E.Ajouter_Piece(R2)

#Noir
#Créer pièces
#Première ligne
p1 = Piece(" p1", "A7", "P", False)
p2 = Piece(" p2", "B7", "P", False)
p3 = Piece(" p3", "C7", "P", False)
p4 = Piece(" p4", "D7", "P", False)
p5 = Piece(" p5", "E7", "P", False)
p6 = Piece(" p6", "F7", "P", False)
p7 = Piece(" p7", "G7", "P", False)
p8 = Piece(" p8", "H7", "P", False)
#Deuxième ligne
r1 = Piece(" r1", "A8", "R", False)
h1 = Piece(" h1", "B8", "H", False)
b1 = Piece(" b1", "C8", "B", False)
q1 = Piece(" q1", "D8", "Q", False)
k1 = Piece(" k1", "E8", "K", False)
b2 = Piece(" b2", "F8", "B", False)
h2 = Piece(" h2", "G8", "H", False)
r2 = Piece(" r2", "H8", "R", False)
#Ajouter pièces à l'échequier
#Première ligne
E.Ajouter_Piece(p1)
E.Ajouter_Piece(p2)
E.Ajouter_Piece(p3)
E.Ajouter_Piece(p4)
E.Ajouter_Piece(p5)
E.Ajouter_Piece(p6)
E.Ajouter_Piece(p7)
E.Ajouter_Piece(p8)
#Deuxième ligne
E.Ajouter_Piece(r1)
E.Ajouter_Piece(h1)
E.Ajouter_Piece(b1)
E.Ajouter_Piece(q1)
E.Ajouter_Piece(k1)
E.Ajouter_Piece(b2)
E.Ajouter_Piece(h2)
E.Ajouter_Piece(r2)
print(Main())

#=============================================================================
#   
#=============================================================================