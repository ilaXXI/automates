from Transition import *
from Automate import *
def choix_automate (): 
    automate = Automate(0, 0, [], [], [])
    choix = int(input("Quel automate voulez-vous utiliser ? (faites un choix entre 1 et 44) "))
    if choix >= 1 and choix <= 44:
        nomFichier = f"automates_test/A8-{choix}.txt"
        automate = lire_fichier(nomFichier)
        automate.afficherAutomate()
        print(automate.caracteristiques())
    else:
        print("Choix invalide. Veuillez choisir un nombre entre 1 et 44.")


def lire_fichier(nomFichier):
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

"""def choix_action():
    choix = int(input("Choisissez une action : \n"
                      "1. Déterminisation de l'automate\n"
                      "2. Standardisation de l'automate\n"
                      "3. Complétion de l'automate\n"
                      "4. Minimisation de l'automate\n"
                      "5. Création du langage complémentaire\n"
                      "Entrez votre choix (1-5) : "))
    if choix == 1:
        #determinisation_automate()
    elif choix == 2:
        #standardisation_automate()
    elif choix == 3:
        #completion_automate()
    elif choix == 4:
        #minimisation_automate()
    elif choix == 5:
        #creation_langage_complementaire()
    else:
        print("Choix invalide. Veuillez entrer un nombre entre 1 et 5.")"""


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

# Début du main
continuer = True
while continuer:
    choix_automate()
    #choix_action()
    reponse = input("Voulez-vous étudier un autre automate ? (Oui/Non): ")
    if reponse.lower() != 'oui':
        continuer = False
print("Fin du programme.")
