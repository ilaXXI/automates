from A8_Transition import *

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
        asynchrone = self.est_asynchrone()        
        
        if asynchrone: # Si l'automate est asynchrone, il y aura une colonne de plus
            tableau = [[" " for i in range(self.nb_symboles + 3)] for i in range(self.nb_etats + 1)]
        else:
            tableau = [[" " for i in range(self.nb_symboles + 2)] for i in range(self.nb_etats + 1)]
        
        for symbole in range(self.nb_symboles): # On liste les symboles de l'alphabet en haut du tableau
            tableau[0][symbole+2] = chr(97+symbole) # (Pour afficher le bon caractère)
        
        if asynchrone: # On rajoute epsilon tout à droite
            tableau[0][self.nb_symboles+2] = "e"

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
            
            if asynchrone: # Si l'automate est asycnhrone, on rajoute ses transitions epsilon
                destinations = self.prochain_etat(etat, -1)
                if len(destinations) != 0:
                    tableau[etat+1][self.nb_symboles+2] = ','.join(str(x) for x in destinations)
                else:
                    tableau[etat+1][self.nb_symboles+2] = "--"


        self.afficherTableau(tableau)

    def est_asynchrone(self):
        for transition in self.transitions:
            if transition.symbole == -1:
                return True
        return False

    def est_deterministe(self): # Renvoie 0 si il y a plusieurs états initiaux, 1 si deux flèches partent du même état avec le même symbole, et 2 si l'automate est déterministe
        
        if len(self.initiaux) > 1: # On vérifie qu'il y a bien un seul état initial
            return 0
        
        if self.est_asynchrone(): # S'il est asynchrone, il n'est pas déterministe
            return 3

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
        
        # Ce suivant tableau correspond à [standard, déterministe, complet]
        # Il permettra de savoir quelles actions peuvent être proposées à l'utilisateur
        caracteristiques = [False, False, False]

        if self.est_asynchrone():
            print("\nL'automate est asynchrone.")
        else:
            print("\nL'automate est synchrone.")

        if self.est_standard():
            caracteristiques[0] = True
            print("L'automate est standard.")
        else:
            print("L'automate n'est pas standard.")

        options = { # Dictionnaire qui répertorie et traite les différents cas pour le déterminisme
            0 : "L'automate n'est pas déterministe, car il existe plusieurs états initiaux.",
            1 : "L'automate n'est pas déterministe, car plusieurs transitions partent du même état avec le même symbole.",
            2 : "L'automate est déterministe.",
            3 : "L'automate n'est pas déterministe, car il est asynchrone."
        }

        est_deterministe = self.est_deterministe()
        print(options[est_deterministe])
        
        if est_deterministe == 2:
            
            caracteristiques[1] = True
            
            if not self.est_complet():
                print("L'automate n'est pas complet.")
            else:
                caracteristiques[2] = True
                print("L'automate est complet.")

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
                    transitions_par_etat[(etat, symbole)] = True

    def standardisation(self) :

        i = self.nb_etats # On crée un nouvel état initial i (en utilisant le nb total d'états dans l'automate)
        self.nb_etats += 1

        term = False
        for etat_initial in self.initiaux : 
            if self.est_etat_terminal(etat_initial) : # On vérifie si le nouvel état initial est terminal
                term = True
        
        if term : # Si au moins un état initial est terminal Alors le nouvel état est terminal
            self.terminaux.append(i)

        transitions_nouv = [] # On crée une nouvelle liste pour stocker les nouvelle transitions
        for transition in self.transitions : # Si un des états de transition est un état initial qui existe Alors on met à jour les états pour pointer vers le nouvel état initial
            if transition.etat1 in self.initiaux :  
                transition.etat1 = i
            transitions_nouv.append(transition)
        self.transitions = transitions_nouv

        self.initiaux = [i] # On met à jour la liste des états initiaux 

    def reconnaissance(self,chaine) : 

        # On initialise l'état de départ à l'état initial
        etat_de_depart = self.initiaux[0]

        # On parcourt la chaine de caractères
        for lettre in chaine :
            #On la convertit en chiffre
            chiffre = ord(lettre)-97

            # On va chercher l'état d'arrivée s'il existe qui devient notre nouvel état de départ
            transition_existe = False 
            for transition in self.transitions :
                if transition.etat1 == etat_de_depart and transition.symbole == chiffre : 
                    etat_de_depart = transition.etat2
                    transition_existe = True
                    break # On sort de la boucle car on a trouvé
            if not transition_existe:
                return False
            
        # On regarde si l'état sur lequel on arrive est terminal
        if etat_de_depart not in self.terminaux : 
            return False

        return True


    def complementarisation(self) : 
        
        #On définit les états non terminaux en soustrayant les états terminaux du nombre d'états total
        non_terminaux = set(range(self.nb_etats)) - set(self.terminaux)

        #On définit les nouveaux états terminaux qui sont les anciens états non terminaux définis précédemment 
        self.terminaux = list(non_terminaux)

    def epsilon_cloture(self, etats):
        # Algorithme pour fermer un ensemble d'états ε
        fermeture = set(etats) # Ensemble des états dans la cloture
        stack = list(etats) # liste des états que l'on a pas encore traités

        while stack:
            etat = stack.pop()
            for transition in self.transitions:
                if transition.etat1 == etat and transition.symbole == -1: # Si un état a une transition ε vers un autre état, on le rajoute dans la cloture
                    etat_suivant = transition.etat2
                    if etat_suivant not in fermeture: # Si on peut rajouter des états déjà dans la cloture, on risquerait de boucler à l'infini
                        fermeture.add(etat_suivant)
                        stack.append(etat_suivant)

        return fermeture

    def calculer_transitions(self, ensemble_etats, symbole): # Calculer les transitions pour un ensemble d'états donné et un symbole donné
        etats_suivants = set()
        for transition in self.transitions:
            if transition.etat1 in ensemble_etats and transition.symbole == symbole:
                etats_suivants.add(transition.etat2)
        return self.epsilon_cloture(etats_suivants)

    def determinisation_completion(self):
        
        etats_non_traites = [set(self.initiaux)]
        etats_traites = []
        transitions = []
        terminaux = []

        while etats_non_traites:
            ensemble_etats = self.epsilon_cloture(etats_non_traites.pop()) # Un ensemble d'états de l'automate de base qui devient un état dans l'AFDC
            etats_traites.append(ensemble_etats)
            if bool(set(ensemble_etats) & set(self.terminaux)): # Si un des états dans l'ensemble est terminal
                terminaux.append(ensemble_etats)                # L'ensemble devient un état terminal

            for symbole in range(self.nb_symboles):
                etats_suivants = self.calculer_transitions(ensemble_etats, symbole)
                if etats_suivants:
                    transitions.append(Transition(ensemble_etats, symbole, etats_suivants))
                    if (etats_suivants not in etats_non_traites) and (etats_suivants not in etats_traites):
                        etats_non_traites.append(etats_suivants)
        

        table_correspondance = {} 

        nb_etats = 0
        for etat in etats_traites: # On cherche maintenant à renommer les états avec des numéros
            
            table_correspondance[nb_etats] = etat
            
            if etat in terminaux: # Si l'état est terminal, on va le trouver et le renommer dans le tableaux des terminaux
                for i in range(len(terminaux)):
                    if terminaux[i] == etat:
                        terminaux[i] = nb_etats
                        break
            
            for transition in transitions: # On renomme les états dans les transitions
                if transition.etat1 == etat:
                    transition.etat1 = nb_etats
                if transition.etat2 == etat:
                    transition.etat2 = nb_etats

            nb_etats += 1

        self.nb_etats = nb_etats 
        self.initiaux = [0]
        self.terminaux = terminaux
        self.transitions = transitions

        if not self.est_complet():
            self.completion()

        return table_correspondance


    def minimisation(self):
        # On sépare les groupes terminaux et les groupes non terminaux 
        terminaux = set(self.terminaux)
        non_terminaux = set(range(self.nb_etats)) - terminaux

        # On crée notre premier groupe de notre itération 0 
        groupes = [terminaux, non_terminaux] 

        if terminaux == set():
            groupes.pop(0)
        if non_terminaux == set():
            groupes.pop(1)

        # On va itérer jusqu'à ce qu'il n'y ait plus de séparation de groupes possible
        while True:
            # On initialise une liste pour stocker les nouveaux groupes à chaque itération
            nouveaux_groupes = []  
            

            for groupe in groupes:
                # On crée un dictionnaire pour stocker les transitions de chaque état du groupe pour chaque symbole de l'alphabet de l'automate
                transitions_groupes = {symbole: [] for symbole in range(self.nb_symboles)}
            
                for etat in groupe:
                    for symbole in range(self.nb_symboles):
                        # On récupère la destination de chaque état pour chaque symbole de l'alphabet
                        destination = self.prochain_etat(etat, symbole)
                        for g in range(len(groupes)):
                            # Si la destination est dans le groupe, on ajoute le groupe dans le dictionnaire
                            if destination[0] in groupes[g]:
                                transitions_groupes[symbole].append(groupes[g])
                                break
                
                for symbole, destinations in transitions_groupes.items():
                    # Si les destinations sont dans plusieurs groupes, on sépare le groupe en plusieurs groupes
                    ensemble_destinations = {tuple(ensemble) for ensemble in destinations}
                    if len(ensemble_destinations) > 1:
                        
                        for dest in ensemble_destinations:
                            # On crée des nouveaux groupes en fonction des destinations
                            nouveaux_groupes.append(set(list(groupe)[i] for i in range(len(groupe)) if destinations[i] == set(dest)))
                        break
                else:
                    nouveaux_groupes.append(groupe)  
            
            # Si aucun groupe créé on sort de la boucle
            if nouveaux_groupes == groupes :
                break 
                
            # On met à jour les groupes
            groupes = nouveaux_groupes[:]

        if len(groupes) == self.nb_etats: # Si on a le même nombre d'etats qu'avant, c'est que c'etait deja minimisé
            return [], False
        
        # On crée un dictionnaire pour stocker la correspondance entre les anciens et les nouveaux noms des états
        table_correspondance = {} 
        
        initiaux = [] # On va changer les états initiaux et terminaux, et les transitions
        terminaux = []

        nb_etats = 0
        
        for groupe in groupes:
            if (groupe & set(self.initiaux)): # Si le groupe d'etats contient l'etat initial, il consititue le nouvel etat initial
                initiaux.append(nb_etats)

            if (groupe & set(self.terminaux)): # De même s'il possède un état terminal, il devient terminal
                terminaux.append(nb_etats)          

            table_correspondance[nb_etats] = groupe

            nb_etats += 1

        for transition in self.transitions: # On refait toutes les transitions une par une avec les nouveaux noms d'etats
            for i in range(nb_etats):
                if transition.etat1 in table_correspondance[i]:
                    transition.etat1 = i
                    break
            for i in range(nb_etats):
                if transition.etat2 in table_correspondance[i]:
                    transition.etat2 = i
                    break            

        for transition1 in range(len(self.transitions)): # On supprime les doublons
            transition2 = transition1+1
            while transition2 < len(self.transitions):
                if self.transitions[transition1].etat1 == self.transitions[transition2].etat1 and self.transitions[transition1].symbole == self.transitions[transition2].symbole:
                    self.transitions.pop(transition2)
                else:
                    transition2 += 1

        self.initiaux = initiaux
        self.terminaux = terminaux
        self.nb_etats = len(groupes)

        
        return table_correspondance, True

    


 
        

        

        

        
    
    



