import sys
import numpy as np
import math
import csv
import fct_calculs_diedres as fct

def squelette_peptidique(file):
    """Récupération des coordonnées du squelette peptidique
    Entrée : file, un fichier gro

    Sortie :
        fichier_squelette : Fichier texte contenant les informations du squelette peptidique
        full_coords : Liste contenant les informations du squelette peptidique
    """
    SQUELETTE = ["C", "N", "CA"]

    with open(f"Coords_squelette_{file[:-4]}.txt", 'w') as fichier_squelette:
        full_coords = []
        print(f"Processing {file}")
        with open(file, 'r') as fichier:

            # Lecture des lignes une à un
            for ligne in fichier:
                ligne_liste = ligne.split()

                # Sélection seulement des coordonnées des N, C, Calpha
                if len(ligne_liste) > 1:
                    if ligne_liste[1] in SQUELETTE:
                        full_coords.append(ligne_liste[:6]) # on récupère les coordonnées x, y et z de l'atome de la ligne
                        
                        # Écriture des coordonnées dans fichier texte
                        fichier_squelette.write(f'{"  ".join(ligne_liste[:6])}\n')
    print(f"Le fichier Coords_squelette_{file[:-4]}.csv a été créé.")
    return(full_coords)


def angle_diedre_csv(coordonnees, file):
    """Écrit dans un fichier csv les angles phi et psi calculés

    Entrée : coordonnees, un numpy array des infos totales du squelette peptidique de dimensions 48 x 6
    
    Sortie : Fichier csv des résidus et leurs angles phi et psi de dimensions 16 x 6
    """
    with open(f"Angles_{file[:-4]}.csv", "w") as fichier:
        colonnes = ["Residus", "Angle phi", "Angle psi"]
        writer = csv.DictWriter(fichier, colonnes)
        writer.writeheader()

        coords = coordonnees[:, -3:].astype(float)
        for i in range(1, len(coords), 3):
            N, CA, C2 = coords[i-1], coords[i], coords[i+1]

            # ========== calcul de phi ==========
            if i-1 == 0:
                phi = "NULL"
            else:
                C = coords[i-2]
                phi = fct.calc_diedre(C, N, CA, C2)
            
            # ========== calcul de psi ==========
            if i+2 == len(coords):
                psi = "NULL"
            else:
                N2 = coords[i+2]
                psi = fct.calc_diedre(N, CA, C2, N2)
            
            nom_res = coordonnees[i, 0][-3:]
            writer.writerow({"Residus": nom_res, "Angle phi": phi, "Angle psi": psi})
    print(f"Le fichier Angles_{file[:-4]}.csv a été créé.")


if __name__ == "__main__":
    # Saisie de tous les fichiers sauf script
    files = sys.argv[1:]
    if not files:
        print("Pas de fichier donné.")
    else:
        for file in files:
            coords_squelette = squelette_peptidique(file)
            coords_squelette = np.array(coords_squelette)
            angle_diedre_csv(coords_squelette, file)
