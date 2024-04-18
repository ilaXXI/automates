from Transition import *

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
        
        # On rajoute un autre etat p qui remplace les vides
        p = self.nb_etats # Le nombre d'état correspond au numéro d'état de p puisque les états sont numérotés à partir de 0
        self.nb_etats += 1

        # On fait une liste des transitions par état
        transitions_par_etat = {} # Dictionnaire qui stocke les transitions par état de départ et symbole
        
        for transition in self.transitions: # On parcourt toutes les transitions
            
            etat_depart = transition.etat1
            symbole = transition.symbole

            if (etat_depart, symbole) not in transitions_par_etat: # On vérifie qu'il n'y soit pas déjà
                transitions_par_etat[(etat_depart, symbole)] = True # On le rajoute dans le dictionnaire
            
                # On fait une double boucle pour trouver les transitions manquantes
        for etat in range(self.nb_etats):
            for symbole in range(self.nb_symboles):
                # S'il manque un symbole pour un état de départ on l'ajoute au tableau de transitions avec comme état d'arrivée p
                if (etat,symbole) not in transitions_par_etat:
                    newTrans = Transition(etat, symbole, p)
                    self.transitions.append(newTrans)

    def standardisation(self) :

        i = self.nb_etats # On crée un nouvel état initial i (en utilisant le nb total d'états dans l'automate)
        self.nb_etats += 1

        term = False
        for etat_initial in self.initiaux : 
            if self.est_etat_terminal(etat_initial) : #on vérifie si le nouvel état initial est terminal
                term = True
        
        if term : #si au moins un état initial est terminal Alors le nouvel état est terminal
            self.terminaux.append(i)

        transitions_nouv = [] #on crée une nouvelle liste pour stocker les nouvelle transitions
        for transition in self.transitions : #si un des états de transition est un état initial qui existe Alors on met à jour les états pour pointer vers le nouvel état initial
            if transition.etat1 in self.initiaux :  
                transition.etat1 = i
            if transition.etat2 in self.initiaux :
                transition.etat2 = i
            transitions_nouv.append(transition)
        self.transitions = transitions_nouv

        self.initiaux = [i] #on met à jour la liste des états initiaux 

    
    def reconnaissance(self,chaine) : 
        
        #if self.est_deterministe == False : 
        #    self.determinisation

        if self.est_complet == False :
            self.completion 

        transitions_par_etat = {} # Dictionnaire qui stocke les transitions par état de départ et symbole
        
        for transition in self.transitions: # On parcourt toutes les transitions
            
            etat_depart = transition.etat1
            symbole = transition.symbole

            if (etat_depart, symbole) not in transitions_par_etat: # On vérifie qu'il n'y soit pas déjà
                transitions_par_etat[(etat_depart, symbole)] = True # On le rajoute dans le dictionnaire

        #On initialise l'état de départ à l'état initial
        etat_de_depart = self.initiaux

        #On parcourt la chaine de caractères
        for lettre in chaine :
            #On la convertit en chiffre
            chiffre = ord(lettre)-97
            #On regarde si elle fait partie des transitions à partir de l'état de départ
            if (etat_de_depart,chiffre) not in transitions_par_etat : 
                return False
            #Si elle en fait bien partie on trouve l'état d'arrivée qui devient notre nouvel état de départ
            else : 
                for transition in self.transitions :
                    if transition.etat1 == etat_de_depart and transition.symbole == chiffre : 
                        etat_de_depart = transition.etat2
                        break #On sort de la boucle car on a trouvé
        
        #On regarde si l'état sur lequel on arrive est terminal
        if etat_de_depart not in self.terminaux : 
            return False

        return True

    def determinisation(self) :
        self.terminaux, self.initiaux = self.initiaux, self.terminaux #on permute les états terminaux en états non terminaux et vice versa

        #si l'automate n'est pas deterministe complet alors il faut d'abord le determiniser puis le compléter si besoin
        if not self.est_deterministe == 2 :
            self.determinisation()
        
        if not self.est_complet() :
            self.completion()

        
        return True

    def complementarisation(self) : 

        #On vérifie que l'automate est déterministe et complet pour pouvoir faire son complémentaire
        if self.est_deterministe != 2 and not self.est_complet : 
            print("Complémentarisation impossible car l'auntomate n'est pas déterministe et complet.")
            return None
        
        #On crée un nouvel automate qui reconnait le langage complementaire de l'automate donné
        auto_complementaire = Automate(nb_symboles=self.nb_symboles, nb_etats=self.nb_etats, initiaux=self.initiaux, terminaux=self.terminaux, transitions=self.transitions)

        #On définit les états non terminaux en soustrayant les états terminaux du nombre d'états total
        non_terminaux = set(range(auto_complementaire.nb_etats)) - set(auto_complementaire.terminaux)

        #On définit les nouveaux états terminaux qui sont les anciens états non terminaux définis précédemment 
        auto_complementaire.terminaux = list(non_terminaux)

        return auto_complementaire
    

    def minimisation(self) : #On suivra l'algorithme de Moore
        #Il n'y a pas de tests à faire car la fonction prend un automate déterministe complet (selon l'énoncé)
        #On va créer un nouvel automate pour pouvoir le retourner en tant qu'automate minimal 
        auto_minimal = Automate(nb_symboles=self.nb_symboles, nb_etats=self.nb_etats, initiaux=self.initiaux, terminaux=self.terminaux, transitions=self.transitions)

        #On a besoin de séparer les états terminaux et les états non terminaux 
        #Les états terminaux étant déjà regroupés dans l'attributs terminaux de l'automate on va séparer les états non terminaux 
        non_terminaux = set(range(auto_minimal.nb_etats)) - set(auto_minimal.terminaux)

        return auto_minimal

        
    
    



