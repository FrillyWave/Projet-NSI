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

    def __repr__(self):
        return f"Echequier : {self.Contenue}"

#=============================================================================
#ZONE TEST
#=============================================================================

Zone_test = Echequier()

BP1 = Piece("BP1", "C2", "P", True)
BP2 = Piece("BP2", "D2", "P", True)
NP1 = Piece("NP1", "D3", "P", False)
BR1 = Piece("BR1", "C3", "R", True)


Zone_test.Ajouter_Piece(BP1)
Zone_test.Ajouter_Piece(BP2)
Zone_test.Ajouter_Piece(NP1)
Zone_test.Ajouter_Piece(BR1)


print(Zone_test.Affichage_provisoire())

print("BP1 : ", BP1.Mouvement_Possible(Zone_test))
print("BP2 : ", BP2.Mouvement_Possible(Zone_test))
print("NP1 : ", NP1.Mouvement_Possible(Zone_test))
print("BR1 : ", BR1.Mouvement_Possible(Zone_test))

#=============================================================================
#
#=============================================================================