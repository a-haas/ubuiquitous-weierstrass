# coding: utf8
from subprocess import call
import argparse
import os

# parsing des arguments
parser = argparse.ArgumentParser("ubiquitous-weierstrass")
# nombre de runs
parser.add_argument("-n", help="Le nombre de fois que le programme iweierstrass sera lancé", type=int)
parser.add_argument("--nbrun", help="Le nombre de fois que le programme iweierstrass sera lancé", type=int)
# dossier des résultats
parser.add_argument("-d", help="Le dossier contenant les résultats du programme iweierstrass", type=str)
parser.add_argument("--directory", help="Le dossier contenant les résultats du programme iweierstrass", type=str)
args = parser.parse_args()

# création du dossier qui va contenir les résultats(si nécessaire sinon on le vide)
res_directory = (args.d or args.directory or "results")
if not os.path.exists(res_directory):
    os.makedirs(res_directory)
else:
    call(["rm", "-f", res_directory +"/*"])
# séléction du nombre de runs, par défaut 20 (pourrait tout aussi bien être 30)
nb_of_runs = (args.n or args.nbrun or 20)

# execution du programme EASEA (transpile > compile)
call(["easea", "iweierstrass.ez"])
call(["make"])
# exécution + sauvegarde des résultats n fois
for n in range(1, nb_of_runs+1):
    with open(res_directory +"/iweierstrass_" +str(n) +".dat", "w") as res_file:
        # execution du programme EASEA (execute)
        call(["./iweierstrass"])
        # récupération des résultats
        with open('iweierstrass.dat', 'r') as easea_file:
            res_file.write(easea_file.read())

# maintenant on peut clean le repository
call(["make", "clean"])
call(["rm","iweierstrass.cpp" ,"iweierstrass.dat", "iweierstrassIndividual.cpp",
      "iweierstrassIndividual.hpp", "iweierstrass.mak", "iweierstrass.prm", "Makefile"])
