from Transition import *
from Automate import *
<<<<<<< HEAD
def choix_automate (): 
    automate = Automate(0, 0, [], [], [])
    choix = int(input("Quel automate voulez-vous utiliser ? (faites un choix entre 1 et 44) "))
    if choix >= 1 and choix <= 44:
        nomFichier = f"automates_test/A8-{choix}.txt"
        automate = lire_fichier(nomFichier)
        automate.afficherAutomate()
        print(automate.caracteristiques())
        return automate
    else:
        print("Choix invalide. Veuillez choisir un nombre entre 1 et 44.")
=======
>>>>>>> origin/main

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

<<<<<<< HEAD
def choix_action(automate):
    choix = int(input("Choisissez une action : \n"
                      "1. Déterminisation de l'automate\n"
                      "2. Standardisation de l'automate\n"
                      "3. Complétion de l'automate\n"
                      "4. Minimisation de l'automate\n"
                      "5. Création du langage complémentaire\n"
                      "Entrez votre choix (1-5) : "))
    if choix == 1:
        #automate.determinisation()
    elif choix == 2:
        #automate.standardisation()
    elif choix == 3:
        automate.completion()
    elif choix == 4:
        #automate.minimisation()
    elif choix == 5:
        automate.complementarisation()
    else:
        print("Choix invalide. Veuillez entrer un nombre entre 1 et 5.")


#Test avec un automate inventé
init = [2]
term = [2, 3]
trans1 = Transition(2, 0, 1)
trans2 = Transition(2, 1, 2)
trans3 = Transition(0, 1, 0)
trans4 = Transition(1, 0, 2)
trans_tab = [trans1, trans2, trans3, trans4]
auto = Automate(3, 4, init, term, trans_tab)

auto.afficherAutomate()
print(auto.est_deterministe())
auto.complementarisation()
auto.afficherAutomate()
=======
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
                #determinisation()
        elif choix == "DC":
            if not (caracteristiques[1] and caracteristiques[2]): # On s'assure que l'automate n'est bien pas déterministe complet
                #standardisation()
        elif choix == "M":
            if not caracteristiques[3]: # On s'assure que l'automate n'est bien pas minimal
                #completion()
        
        print("Choix invalide. Réessayez.")
"""
>>>>>>> origin/main

# Début du main
continuer = True
while continuer:
<<<<<<< HEAD
    automate = choix_automate()
    #choix_action(automate)
=======
    auto = choix_automate()
    auto.afficherAutomate()
    caracteristiques = auto.caracteristiques()
    #choix_action(auto, caracteristiques)
>>>>>>> origin/main
    reponse = input("Voulez-vous étudier un autre automate ? (Oui/Non): ")
    if reponse.lower() != 'oui':
        continuer = False
print("Fin du programme.")
