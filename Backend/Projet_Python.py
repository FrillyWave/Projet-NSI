#Class pièce 

def coordonnees_to_case(liste):
    for i in range(len(liste)):
        nombre = 7 - liste[i][1]
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

    def translate_coordonnees(self):
        x = ord(self.Position[0]) - 65
        y = abs(int(self.Position[1]) - 8)
        return x,y 

    def Mouvement_Possible(self, Echequier):
        echequier = Echequier.GetContenue()  
        liste_mouvements = []
        piece_type = self.GetType()
        piece_position = self.translate_coordonnees()
        piece_color = self.GetCouleur()

        #Pion
        if piece_type == "P":
            # avance 1 case classique 
            if piece_color:
                if echequier[piece_position[1] - 1][piece_position[0]] == None:
                    liste_mouvements.append((piece_position[0], piece_position[1] - 1))
            else:
                if echequier[piece_position[1] + 1][piece_position[0]] == None:
                    liste_mouvements.append((piece_position[0], piece_position[1] + 1))
            # avance 2 cases au début
            if piece_color:
                if piece_position[1] == 6 and (echequier[piece_position[1] - 1][piece_position[0]] == None and echequier[piece_position[1] - 2][piece_position[0]] == None):
                    liste_mouvements.append((piece_position[0], piece_position[1] - 2))
            else:
                if piece_position[1] == 1 and (echequier[piece_position[1] + 1][piece_position[0]] == None and echequier[piece_position[1] + 2][piece_position[0]] == None):
                    liste_mouvements.append((piece_position[0], piece_position[1] + 2))
            # manger en diagonale
            # en passant

        # King
        if piece_type == "K":
            # Haut Gauche
            if piece_position[1] - 1 >= 0 and piece_position[0] - 1 >= 0:
                liste_mouvements.append((piece_position[0] - 1, piece_position[1] - 1))
            # Haut 
            if piece_position[1] - 1 >= 0:
                liste_mouvements.append((piece_position[0], piece_position[1] - 1))
            # Haut droite
            if piece_position[1] - 1 >= 0 and piece_position[0] + 1 <= 7:
                liste_mouvements.append((piece_position[0] + 1, piece_position[1] - 1))
            # Gauche
            if piece_position[0] - 1 >= 0:
                liste_mouvements.append((piece_position[0] - 1, piece_position[1]))
            # Bas Gauche
            if piece_position[0] - 1 >= 0 and piece_position[1] + 1 <= 7:
                liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 1))
            # Bas
            if piece_position[1] + 1 <= 7:
                liste_mouvements.append((piece_position[0], piece_position[1] + 1))
            # Bas Droite
            if piece_position[0] - 1 >= 0 and piece_position[1] + 1 <= 7:
                liste_mouvements.append((piece_position[0] - 1, piece_position[1] + 1))
            # Droite 
            if piece_position[0] + 1 <= 7 :
                liste_mouvements.append((piece_position[0] + 1, piece_position[1] + 1))

        #Rook
        if piece_type == "R":
            # Haut 
            pass


            






    
        





        
        return coordonnees_to_case(liste_mouvements)

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

BP1 = Piece('BP1', 'B2', 'P', True)
NP2 = Piece('NP2', 'B4', 'P', False)
BK1 = Piece('BK1', 'E8', 'K', True)
print(BP1)
E = Echequier()
print(E)
E.Ajouter_Piece(BK1)
E.Ajouter_Piece(BP1)
E.Ajouter_Piece(NP2)
print(E.Affichage_provisoire())
print(BP1.Mouvement_Possible(E))
print(NP2.Mouvement_Possible(E))
print(BK1.Mouvement_Possible(E))
