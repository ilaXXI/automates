from Transition import *
from Automate import *

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

"""
def choix_action(caracteristiques): # Permet à l'utilisateur de choisir une action
    
    choix_invalide = True
    while choix_invalide:

        print("Choisissez une action : \n")
        
        if not caracteristiques[0]: # Si l'automate n'est pas standard
            print("S - Standardisation de l'automate")

        if not (caracteristiques[1] and caracteristiques[2]): # Si l'automate n'est pas déterministe complet
            print("DC - Obtention de l'automate deterministe complet équivalent")

        if not (caracteristiques[3]):
            print("M - Minimisation de l'automate\n")


        choix = input("Votre choix : ").lower
        if choix == "S":
            if not caracteristiques[0]: # On s'assure que l'automate n'est bien pas standard
                #determinisation_automate()
        elif choix == "DC":
            if not (caracteristiques[1] and caracteristiques[2]): # On s'assure que l'automate n'est bien pas déterministe complet
                #standardisation_automate()
        elif choix == "M":
            if not caracteristiques[3]: # On s'assure que l'automate n'est bien pas minimal
                #completion_automate()
        
        print("Choix invalide. Réessayez.")
"""

# Début du main
continuer = True
while continuer:
    auto = choix_automate()
    auto.afficherAutomate()
    caracteristiques = auto.caracteristiques()
    auto.completion()
    auto.afficherAutomate()
    #choix_action(auto, caracteristiques)
    reponse = input("Voulez-vous étudier un autre automate ? (Oui/Non): ")
    if reponse.lower() != 'oui':
        continuer = False
print("Fin du programme.")
