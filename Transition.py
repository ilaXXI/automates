class Transition:
    def __init__(self, etat1, symbole, etat2):
        self.etat1 = etat1
        self.etat2 = etat2
        self.symbole = symbole