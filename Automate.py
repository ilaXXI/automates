class Automate:
    def __init__(self, nb_symboles, nb_etats, initiaux, terminaux, transitions):
        
        self.nb_symboles = nb_symboles
        self.nb_etats = nb_etats
        self.initiaux = initiaux
        self.terminaux = terminaux
        self.transitions = transitions

    def est_etat_terminal(self, etat):
        return etat in self.terminaux

    def est_etat_initial(self, etat):
        return etat in self.initiaux

    def prochain_etat(self, etat, symbole): # Renvoie un tableau avec les destinations possibles depuis un état avec un symbole
        destinations = []
        for t in self.transitions:
            if t.etat1 == etat:
                if t.symbole == symbole:
                    destinations.append(t.etat2)
        return sorted(destinations)


    def afficherTableau(self, tab): # Fonction qui permet d'afficher un tableau de manière jolie et sans décalage
        max_largeurs = [max(len(str(cellule)) for cellule in colonne) for colonne in zip(*tab)]
        for ligne in tab:
            print("|", end="")
            for cellule, largeur_max in zip(ligne, max_largeurs):
                print(f" {str(cellule).ljust(largeur_max)} |", end="")
            print("\n" + "-" * (sum(max_largeurs) + len(max_largeurs) * 3 + 1))

    def afficherAutomate(self):
        tableau = [[" " for i in range(self.nb_symboles + 2)] for i in range(self.nb_etats + 1)]

        for symbole in range(self.nb_symboles): # On liste les symboles de l'alphabet en haut du tableau
            tableau[0][symbole+2] = chr(97+symbole) # (Pour afficher le bon caractère)
        
        for etat in range(self.nb_etats): # On remplit ligne par ligne
            
            if self.est_etat_initial(etat): # On précise si l'état est une entrée et/ou une sortie
                tableau[etat+1][0] = "E"
            if self.est_etat_terminal(etat):
                if tableau[etat+1][0] == "E":
                    tableau[etat+1][0] = "E/S"
                else:
                    tableau[etat+1][0] = "S"

            tableau[etat+1][1] = etat # On donne le numéro de l'état

            for symbole in range(self.nb_symboles): # On note les transitions à partir de chaque état pour chaque symbole
                destinations = self.prochain_etat(etat, symbole)
                if len(destinations) != 0:
                    tableau[etat+1][symbole+2] = ','.join(str(x) for x in destinations)
                else:
                    tableau[etat+1][symbole+2] = "--"

        self.afficherTableau(tableau)


    def est_deterministe(self): # Renvoie 0 si il y a plusieurs états initiaux, 1 si deux flèches partent du même état avec le même symbole, et 2 si l'automate est déterministe
        
        if len(self.initiaux) > 1: # On vérifie qu'il y a bien un seul état initial
            return 0
        
        transitions_par_etat = {} # Dictionnaire qui stocke les transitions par état de départ et symbole
        
        for transition in self.transitions: # On parcourt toutes les transitions
            
            etat_depart = transition.etat1
            symbole = transition.symbole

            if (etat_depart, symbole) in transitions_par_etat: # On vérifie qu'il n'y ait pas une transition avec le même état1 et symbole
                return 1
            else:
                transitions_par_etat[(etat_depart, symbole)] = True # Sinon on le rajoute dans le dictionnaire

        return 2

    def est_complet(self): 

        #Un automate est complet s'il est déterministe et si à partir de chaque état on arrive dans un autre état (potentiellement le même) avec tous les symboles de l'alphabet

        #On regarde si le nombre de transitions vérifie l'équation : nb_transitions = nb_états*nb_symboles (l'automate est déterministe)
        if len(self.transitions) != (self.nb_symboles*self.nb_etats) : 
            return False
        
        return True
    
    def est_standard(self) :

        # Un automate est standard s'il n'a qu'une seule entrée et si aucune autre transition n'aboutit à cette entrée 

        # On vérifie qu'il n'y a qu'une seule entrée
        if len(self.initiaux) != 1 :
            return False

        unique_entree = self.initiaux[0]

        # On vérifie qu'il n'y a aucune transition aboutissant à cette unique entrée
        for transition in self.transitions :
            if transition.etat2 == unique_entree :
                return False

        return True

    def caracteristiques (self) : # Affiche les caractéristiques de l'automate
        
        # Ce suivant tableau correspond à [standard, déterministe, complet, minimisé]
        # Il permettra de savoir quelles actions peuvent être proposées à l'utilisateur
        caracteristiques = [False, False, False, False]

        #est_minimal = self.est_minimal()

        if self.est_standard():
            caracteristiques[0] = True
            print("\nL'automate est standard.")
        else:
            print("\nL'automate n'est pas standard.")

        options = { # Dictionnaire qui répertorie et traite les différents cas pour le déterminisme
            0 : "L'automate n'est pas déterministe, car il existe plusieurs états initiaux.",
            1 : "L'automate n'est pas déterministe, car plusieurs transitions partent du même état avec le même symbole.",
            2 : "L'automate est déterministe."
        }

        est_deterministe = self.est_deterministe()
        print(options[est_deterministe])
        
        if est_deterministe == 2:
            
            caracteristiques[1] = True
            
            if self.est_complet():
                caracteristiques[2] = True
                print("L'automate est complet.")
            else:
                print("L'automate n'est pas complet.")

        return caracteristiques

            

    def completion(self): 

        #On regarde si l'automate est complet, le cas échéant pas besoin de le compléter
        if self.est_complet:
            return
        
        #On rajoute un autre etat p qui remplace les vides
        p = self.nb_etats #le nombre d'état correspond au numéro d'état de p puisque les états sont numérotés à partir de 0

        #On fait une liste des transitions par état
        transitions_par_etat = {} # Dictionnaire qui stocke les transitions par état de départ et symbole
        
        for transition in self.transitions: # On parcourt toutes les transitions
            
            etat_depart = transition.etat1
            symbole = transition.symbole

            if (etat_depart, symbole) not in transitions_par_etat: #On vérifie qu'il n'y soit pas déjà
                transitions_par_etat[(etat_depart, symbole)] = True #On le rajoute dans le dictionnaire

        #On fait une liste des états
        liste_des_etats = {}
        
        #On parcourt la liste des transitions pour compléter la liste
        
        #On le fait une première fois avec les états de départ
        for transition in self.transitions: # On parcourt toutes les transitions
            
            etat_depart = transition.etat1

            if (etat_depart) not in liste_des_etats: # On vérifie qu'il n'est pas déjà dans la liste
                liste_des_etats[(etat_depart)] = True 

        #On le fait une deuxième fois avec les états d'arrivée
        for transition in self.transitions: # On parcourt toutes les transitions
            
            etat_arrivee = transition.etat2

            if (etat_arrivee) not in liste_des_etats: # On vérifie qu'il n'est pas déjà dans la liste
                liste_des_etats[(etat_arrivee)] = True 

        #On fait une liste des symboles
        liste_des_symboles ={}

        #On parcourt la liste des transitions pour compléter la liste
        for transition in self.transitions: # On parcourt toutes les transitions
            
            symbole= transition.symbole

            if (symbole) not in liste_des_symboles: # On vérifie qu'il n'est pas déjà dans la liste
                liste_des_symboles[(symbole)] = True 


        #On fait une double boucle pour trouver les transitions manquantes
        for etat in liste_des_etats:
            for symbole in liste_des_symboles:
                #si il manque un symbole pour un état de départ on l'ajoute au tableau de transitions avec comme état d'arrivée p
                if (etat,symbole) not in transitions_par_etat:
                    self.transitions[(etat,symbole,p)]=True
