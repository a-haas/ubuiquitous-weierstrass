# coding: utf8
from subprocess import call
import argparse
import os
import threading

# UTILS FUNCTIONS
"""
exec_easea
Fonction permettant d'executer + récupérer le résultat du programme EASEA
"""
def exec_easea(dir, port):
    call(["./iweierstrass", "--serverPort", port], cwd=dir)

# SCRIPT
# parsing des arguments
parser = argparse.ArgumentParser("ubiquitous-weierstrass")
# nombre de runs
parser.add_argument("-n", help="Le nombre de fois que le programme iweierstrass sera lancé", type=int)
parser.add_argument("--nbrun", help="Le nombre de fois que le programme iweierstrass sera lancé", type=int)
# dossier des résultats
parser.add_argument("-d", help="Le dossier contenant les résultats du programme iweierstrass", type=str)
parser.add_argument("--directory", help="Le dossier contenant les résultats du programme iweierstrass", type=str)
# si on veut des ilots
parser.add_argument("-i", help="Le fichier contenant l'adresse des ilots", type=str)
parser.add_argument("--ilots", help="Le fichier contenant l'adresse des ilots", type=str)
args = parser.parse_args()

# création du dossier qui va contenir les résultats(si nécessaire sinon on le vide)
res_directory = (args.d or args.directory or "results")
if not os.path.exists(res_directory):
    os.makedirs(res_directory)
else:
    call(["rm", "-r", "-f", res_directory+"/*"])
# séléction du nombre de runs, par défaut 1 (pourrait tout aussi bien être 30)
nb_of_runs = (args.n or args.nbrun or 1)
# parsing des ilots
filename_ilots = (args.i or args.ilots)
server_ports = []
# si on doit parser les IPs
if filename_ilots is not None:
    # ouverture du fichier (U = universal line support)
    with open(filename_ilots, "rU") as file_ilots:
        # pour chaque ligne du fichier (équivalent à pour chaque IP)
        for line_ilot in file_ilots:
            line_ilot = line_ilot.rstrip('\n')
            # check if the line is not empty
            if line_ilot:
                address, port = line_ilot.split(":")
                server_ports.append(port)

# execution du programme EASEA (transpile > compile)
call(["easea", "iweierstrass.ez"])
call(["make"])
# exécution + sauvegarde des résultats n fois
for n in range(1, nb_of_runs+1):
    # create the directory for the run
    run_directory = res_directory +"/run_" +str(n)
    if not os.path.exists(run_directory):
        os.makedirs(run_directory)
    threads = []
    for port in server_ports:
        # créer le répertoir pour l'ilot
        ilot_directory = run_directory + "/island_" + port
        if not os.path.exists(ilot_directory):
            os.makedirs(ilot_directory)
        call(["cp", "iweierstrass", ilot_directory +"/iweierstrass"])
        call(["cp", "iweierstrass.prm", ilot_directory + "/iweierstrass.prm"])
        # on exécute le programme iweierstrass maintenant
        t = threading.Thread(target=exec_easea, args=(ilot_directory, port))
        threads.append(t)
        t.start()
    # on attend la fin des threads
    for t in threads:
        t.join()

# maintenant on peut clean le repository
call(["make", "clean"])
call(["rm", "-f", "iweierstrass.cpp" ,"iweierstrass.dat", "iweierstrassIndividual.cpp",
      "iweierstrassIndividual.hpp", "iweierstrass.mak", "iweierstrass.prm", "Makefile"])
