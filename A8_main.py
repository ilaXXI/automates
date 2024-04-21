from A8_Transition import *
from A8_Automate import *

def lire_automate(nomFichier): # Renvoie un automate à partir d'un fichier
    
    with open(nomFichier, 'r') as fichier:  # On ouvre le fichier de manière sécurisée
        lignes = fichier.readlines()  # On crée une liste avec les lignes du fichier 

    # On extrait les informations du fichier.txt
    nb_symboles = int(lignes[0])
    nb_etats = int(lignes[1])
    initiaux = list(map(int, lignes[2].split()[1:]))
    terminaux = list(map(int, lignes[3].split()[1:]))
    transitions = []  # On initialise une liste pour stocker les transitions

    # On remplit cette liste grâce à l'extraction des informations à partir de la 6ème ligne du fichier
    for line in lignes[5:]:
        # On divise la ligne en état initial, symbole et état final
        etat_initial, symbole, etat_final = map(int, line.split())
        transitions.append(Transition(etat_initial, symbole, etat_final))


    automate = Automate(nb_symboles, nb_etats, initiaux, terminaux, transitions)
    return automate  

def choix_automate (): 
    reponse_valide = False;
    while not reponse_valide:
        choix = int(input("Quel automate voulez-vous utiliser ? (faites un choix entre 1 et 44)"))
        if choix >= 1 and choix <= 44:
            nomFichier = f"automates_test/A8-{choix}.txt"
            automate = lire_automate(nomFichier)
            return automate
        else:
            print("Choix invalide. Veuillez choisir un nombre entre 1 et 44.")


def choix_action(automate, caracteristiques): # Permet à l'utilisateur de choisir une action
    
    choix_invalide = True
    while choix_invalide:
        
        changement_de_l_automate = True # Si c'est true, l'automate a été modifié

        print("\nChoisissez une action : \n")
        
        if not caracteristiques[0]: # Si l'automate n'est pas standard
            print("S - Standardisation de l'automate")

        if not (caracteristiques[1] and caracteristiques[2]): # Si l'automate n'est pas déterministe complet
            print("DC - Obtention de l'automate deterministe complet equivalent")

        
        print("M - Minimisation de l'automate")

        print("C - Obtention d'un automate reconnaissant le langage complementaire")

        print("R - Test de la reconnaissance d'un mot\n")

        choix = input("Votre choix : ").lower()

        if choix == "s":
            if not caracteristiques[0]: # On s'assure que l'automate n'est bien pas standard
                choix_invalide = False
                automate.standardisation()

        elif (choix == "dc") or (choix == "c") or (choix == "m"):
            if not (caracteristiques[1] and caracteristiques[2]): # On s'assure que l'automate n'est bien pas déterministe complet
                choix_invalide = False
                if caracteristiques[1]: # S'il est déjà déterministe on ne fait que le compléter
                    automate.completion()
                else:
                    table_correspondance = automate.determinisation_completion()
                    print("\nSuite a la determinisation et/ou completion, voici le tableau des relations entre les anciens et nouveaux etats sous la forme (anciens : nouveau)\n\n", table_correspondance)
                if choix == "m":
                    print("\nVoici l'automate deterministe complet : \n")
                    automate.afficherAutomate()

            if choix == "c":
                choix_invalide = False
                print("\nOn obtient l'automate reconnaissant le langage complementaire a partir de l'automate deterministe complet equivalent.")
                automate.complementarisation()

            elif choix == "m":
                choix_invalide = False
                table_correspondance, reussite = automate.minimisation()
                if reussite:
                    print("\nSuite a la minimisation, voici la table de correspondance des anciens etats et les nouveaux, sous la forme (nouveau : anciens)\n\n", table_correspondance)
                else:
                    print("\nL'automate est minimal !\n")
                    changement_de_l_automate = False

        elif choix == "r":
            choix_invalide = False
            changement_de_l_automate = False

            # On crée une copie de l'automate
            automate_dc = Automate(automate.nb_symboles, automate.nb_etats, automate.initiaux, automate.terminaux, automate.transitions)

            if not (caracteristiques[1] and caracteristiques[2]): # S'il le faut on déterminise et complète cet automate, nécéssaire pour la reconnaissance
                if caracteristiques[1]: 
                    automate_dc.completion()
                else:
                    automate_dc.determinisation_completion()            

            chaine = input("Quelle mot voulez-vous tester ? ")
            mot_reconnu = automate_dc.reconnaissance(chaine)
            
            if mot_reconnu:
                print("\nLe mot ", chaine, " est reconnu par l'automate.")
            else:
                print("\nLe mot ", chaine, " n'est pas reconnu par l'automate.")
        
        if choix_invalide:
            print("\nChoix invalide. Reessayez.")
        else:
            return changement_de_l_automate


# Début du main
continuer = True
while continuer:
    
    auto = choix_automate()
    print("\n\n")
    auto.afficherAutomate()
    caracteristiques = auto.caracteristiques()
    
    automate_courant = True # Tant que c'est true, on continue d'étudier cet automate  
    while automate_courant:
        
        changement_de_l_automate = choix_action(auto, caracteristiques)
        if changement_de_l_automate:
            print("\nVoici votre nouvel automate :\n")
            auto.afficherAutomate()
            caracteristiques = auto.caracteristiques()
        
        reponse1 = input("\nVoulez-vous effectuer une autre action ? (Oui/Non): ")
        if reponse1.lower() != 'oui':
            automate_courant = False
    
    reponse2 = input("\nVoulez-vous etudier un autre automate ? (Oui/Non): ")
    if reponse2.lower() != 'oui':
        continuer = False

print("\n\nFin du programme.")
