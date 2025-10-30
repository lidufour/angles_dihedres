import sys
import math
from Bio.PDB import Vector, calc_dihedral
import csv

def squelette_peptidique(file):
    """Récupération des coordonnées du squelette peptidique
    Entrée : file, un fichier gro

    Sortie : atomes : Liste contenant les informations du squelette peptidique
    """
    SQUELETTE = ["C", "N", "CA"]

    atomes = {}
    print(f"Processing {file}")
    with open(file, 'r') as fichier:

        # Lecture des lignes une à un
        for ligne in fichier:
            ligne_liste = ligne.split()

            # Sélection seulement des coordonnées des N, C, Calpha
            if len(ligne_liste) > 1:
                if ligne_liste[1] in SQUELETTE:
                    x, y, z = map(float, ligne_liste[3:6])
                    atomes[f'{ligne_liste[0]}_{ligne_liste[1]}'] = Vector(x, y, z)
    return(atomes)


def angle_diedre_csv(dico_vect, file):
    """Écrit dans un fichier csv les angles phi et psi calculés

    Entrée : Dictionnaire de forme {res_atome : Vector(coordonnées), ect}
    
    Sortie : Fichier csv des résidus et leurs angles phi et psi de dimensions 16 x 6
    """
    with open(f"Angles_biopython_{file[:-4]}.csv", "w") as fichier:
        colonnes = ["Residus", "Angle phi", "Angle psi"]
        writer = csv.DictWriter(fichier, colonnes)
        writer.writeheader()

        cles_res = list(dico_vect.keys())
        for i in range(1, len(cles_res), 3):
            N, CA, C2 = dico_vect[cles_res[i-1]], dico_vect[cles_res[i]], dico_vect[cles_res[i+1]]
            
            # ========== calcul de phi ==========
            if i-1 == 0:
                phi = "NULL"
            else:
                C = dico_vect[cles_res[i-2]]
                phi = calc_dihedral(C, N, CA, C2)
                phi = math.degrees(phi)
            
            # ========== calcul de psi ==========
            if i+2 == len(cles_res):
                psi = "NULL"
            else:
                N2 = dico_vect[cles_res[i+2]]
                psi = calc_dihedral(N, CA, C2, N2)
                psi = math.degrees(psi)
            
            nom_res = cles_res[i][2:5]
            writer.writerow({"Residus": nom_res, "Angle phi": phi, "Angle psi": psi})
    print(f"Le fichier Angles_biopython_{file[:-4]}.csv a été créé.")


if __name__ == "__main__":
    # Saisie de tous les fichiers sauf script
    files = sys.argv[1:]
    if not files:
        print("Pas de fichier donné.")
    else:
        for file in files:
            coords_squelette = squelette_peptidique(file)
            angle_diedre_csv(coords_squelette, file)