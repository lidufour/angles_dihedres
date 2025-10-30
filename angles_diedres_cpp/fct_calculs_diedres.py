import numpy as np
import math


""" Script contenant les fonctions calculatoires pour le projet angles"""

def calc_coords_vec(a1, a2):
    """Calcule les coordonnées du vecteurs associés aux atomes a1 et a2.
    
    Entrée:
    a1, a2: numpy array des coordonnées d'atomes (x, y ,z), format 1x3
    
    Sortie:
    v1: numpy array des coordonnées du vecteur (a1, a2), format 1 x 3"""

    return a2 - a1

def calc_prod_scal(v1, v2):
    """Calcule le produit scalaire des vecteurs v1 et v2.
    
    Entrée: coordonnées des vecteurs v1 et v2;
            numpy array de dimension 1 x 3
    
    Sortie: valeur absolue de la somme des coordonnées des vecteurs;
            float
    
    """

    prod_scal = (v1[0] * v2[0]
                + v1[1] * v2[1]
                + v1[2] * v2[2])
    
    return (prod_scal)
    
def calc_prod_vec(v1, v2):
    """ Calcule le produit vectoriel des vecteurs v1 et v2.
    
    Entrée: vecteurs v1 et v2, numpy array de dimension 1 x 3
    
    Sortie: vecteur normal z de coordonnées i j k; numpy array de dimension 1 x 3."""

    z_i = v1[1]*v2[2] - v2[1]*v1[2]
    z_j = v2[0]*v1[2] - v1[0]*v2[2]
    z_k = v1[0]*v2[1] - v2[0]*v1[1]

    return np.array([z_i, z_j, z_k])

def calc_norm_vec (v):
    """Calcule norme du vecteur v.
    
    Entrée: coordonnées x, y, z du vecteur v;
            numpy array de dimensions 1 x 3
            
    Sortie: norme v_norm du vecteur v;
            float
    """

    v_norm = math.sqrt(v[0]**2 +
                       v[1]**2 +
                       v[2]**2)
    
    return v_norm

def calc_angle_vec (v1, v2):
    """Calcule angle de valence formé par v1 et v2.
    
    Entrée: Coordonnées des vecteurs v1 et v2;
            numpy array de dimension 1 x 3.
    
    Sortie: Valeur de l'angle theta de valence v1 et v2, en radians (à convertir en degrés ?);
            float
    """

    # calcul du cosinus de theta à partir de l'équation de l'angle de valence
    cos_theta = calc_prod_scal(v1, v2) / (calc_norm_vec(v1) * calc_norm_vec(v2)) 
    theta_rad = math.acos(round(cos_theta, 6)) #calcul theta (en radians), arrondi au 6e chiffre après la virgule
    theta_deg = theta_rad * 180 / math.pi #conversion en degrés

    return(theta_deg)

  


def calc_diedre(a1, a2, a3, a4):
    """Calcule l'angle dièdre à partir de 4 atomes consécutifs du squelette.
    pour angle phi: Ci-1, Ni, CAi, Ci;
    pour angle psi: Ni, Ca, Ci, Ni+1

    Entrée : coordonnées de chaque atome;
            a1 : NParray
            a2 : NParray
            numpy array de dimension 3 x 1

    Sortie: angle dièdre associé aux atomes
            float en degrés 
    """
    # plan 1 (a1, a2, a3)
    # vecteurs définissant le plan 1
    v_a1a2 = calc_coords_vec(a1, a2)
    v_a2a3 = calc_coords_vec(a2, a3)
    
    z1 = calc_prod_vec(v_a1a2, v_a2a3) # z1 : vecteur normal du plan 1

    # plan 2 (a2, a3, a4)
    # vecteurs définissant le plan 2
    # v_a2a3 même que pour le plan 1
    v_a3a4 = calc_coords_vec(a3, a4)

    z2 = calc_prod_vec(v_a2a3, v_a3a4)  # z2 : vecteur normal du plan 2

    # normalisation des vecteurs normaux
    z1_norm = z1 / calc_norm_vec(z1)
    z2_norm = z2 / calc_norm_vec(z2)
    v_a2a3_norm = v_a2a3 / calc_norm_vec(v_a2a3)

    # calcul angle dièdre

    # angle formé par les vecteurs normaux z1 et z2
    ang_died = calc_angle_vec(z1, z2)

    # Détermination du signe de l'angle
    signe = calc_prod_scal(calc_prod_vec(z1,z2), v_a2a3_norm) # v1 est le vecteur de référence

    if signe > 0: #si le sens est dans le même sens que le vecteur de référence
        return(ang_died)
    else :
        return(- ang_died)




if __name__ == "__main__":

    ## calc_coords_vec ##########################################################
    a1 = np.array([0,0,0])
    a2 = np.array([1,2,3])

    v1 = calc_coords_vec(a1,a2)
    #print(f"Les coordonnées du vecteur sont x = {v1[0]}, y = {v1[1]}, z = {v1[2]}")
    #print("numpy_array =", v1)

    ## calc_prod_scal ##########################################################

    a3 = np.array([3,2,1])
    v2 = calc_coords_vec(a2, a3)

    #calcul produit scalaire de v1 et v2
    scal_v1v2 = calc_prod_scal(v1, v2)

    #print(f"Le produit scalaire de v1 et v2 vaut = {scal_v1v2}")

    ## calc_prod_vec ##########################################################

    z_coords = calc_prod_vec(v1, v2)
    #print(f"Le vecteur normal du plan formé par v1 et v2 a comme coordonnées : {z_coords}")

    ## calc_norm_vec ##########################################################

    norm_v1 = calc_norm_vec(v1)
    norm_v2 = calc_norm_vec(v2)

    #print(f"norme(v1) = {norm_v1}\nnorme(v2) = {norm_v2}")


    ## calc_angle_vec ##########################################################

    ang_v1v2 = calc_angle_vec(v1, v2)
    #print(f"L'angle de valence formé par v1 et v2 vaut = {ang_v1v2}°.")

    ## calc_diedre ##########################################################

    atom1 = np.array([0,0,0])
    atom2 = np.array([1,1, 1])
    atom3 = np.array([1.5,1.5,1.5])
    atom4 = np.array([2,2,2])

    diedre = calc_diedre(atom1, atom2, atom3, atom4)

    print(f"L'angle dièdre formé par les plans (a1, a2, a3) et (a2, a3, a4) vaut: {diedre}.")

