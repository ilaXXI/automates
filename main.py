from Transition import *
from Automate import *

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