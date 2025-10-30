# Projet : Calcul d’angles dièdres (phi/psi) et visualisation (diagramme de Ramachandran)

Ce projet permet de calculer les angles dièdres (phi et psi) pour les résidus du peptide de pénétration cellulaire (CPP) à partir de fichiers `.gro` générés par GROMACS ou équivalent, puis de comparer ces résultats avec ceux obtenus via BioPython. Enfin, un script R (ramachandran_cpp.R) produit un diagramme de Ramachandran superposant les données.

------------------------------------------------------------------------

## 1. Structure des fichiers

-   **a. Répertoire `angles_diedres_cpp`:\
    **

-   **`fct_calculs_diedres.py`**\
    Contient les fonctions pour calculer :

    1.  Les coordonnées des vecteurs (calc_coords_vec).
    2.  Les produits scalaire et vectoriel (calc_prod_scal, calc_prod_vec).
    3.  L’angle de valence (calc_angle_vec).
    4.  L’angle dièdre (calc_diedre).

-   **`diedre_cpp.py`**

    -   Parcourt un fichier `.gro` passé en argument.
    -   Extrait les coordonnées du squelette peptidique (N, CA, C).
    -   Calcule les angles phi et psi pour chaque résidu (via `fct_calculs_diedres.py`).
    -   Génère un fichier CSV (par exemple `Angles_md.csv`).

-   **`diedre_cpp_biopython.py`**

    -   Fait la même chose que `diedre_cpp.py`, mais utilise BioPython (`Bio.PDB.calc_dihedral`) pour le calcul des angles.
    -   Génère un fichier CSV (`Angles_biopython_start.csv`, `Angles_biopython_md.csv` pour `start.gro` et `md.gro` respectivement), afin de comparer les résultats.

-   **`ramachandran_cpp.R`**

    -   Lit les fichiers CSV générés (angles calculés via le script custom et angles calculés via BioPython).
    -   Trace un diagramme de Ramachandran (phi en abscisse, psi en ordonnée).
    -   Sauvegarde l’image au format PNG (`ramachandran_cpp.png`).

-   **`md.gro`, `start.gro`**

    -   Fichiers de coordonnées (format GROMACS `.gro`) représentant deux états du peptide CPP (conformation initiale vs. après dynamique moléculaire).

-   **`helice_start_end.pse`**

    -   Fichier PyMOL (extension `.pse`) qui peut contenir une visualisation particulière de la protéine (hélices, etc.).\
        *(Ce fichier n’est pas directement utilisé par les scripts de calcul.)*

-   **b. Répertoire `angles_diedres_cpp_avec_output`:\
    **

-   Contient les mêmes fichiers que `angles_diedres_cpp`, mais avec les fichiers générés par les scripts.

-   Cela permet d'avoir accès aux outputs si un script présente une erreur.

-   **`Angles_biopython_start.csv`**

    -   Fichier d'angles dièdres phi et psi du peptide CPP calculés via BioPython à partir du fichier `start.gro`, avant dynamique moléculaire. Généré par `diedre_cpp_biopython.py`.

-   **`Angles_biopython_md.csv`**

    -   Fichier d'angles dièdres phi et psi du peptide CPP calculés via BioPython à partir du fichier `md.gro`, après dynamique moléculaire. Généré par `diedre_cpp_biopython.py`.

-   **`Angles_md.csv`**

    -   Fichier d'angles dièdres phi et psi du peptide CPP calculés via le script custom `fct_calculs_diedres.py` à partir du fichier `md.gro`, après dynamique moléculaire. Généré par `diedre_cpp.py`.

-   **`Angles_start.csv`**

    -   Fichier d'angles dièdres phi et psi du peptide CPP calculés via le script custom `fct_calculs_diedres.py` à partir du fichier `start.gro`, avant dynamique moléculaire. Généré par `diedre_cpp.py`.

-   **`Coords_squelette_md.txt`**

    -   Fichiers de coordonnées des atomes du squelette de la CPP extraits du fichier `md.gro`. Généré par `diedre_cpp.py`.

-   **`Coords_squelette_start.txt`**

    -   Fichiers de coordonnées des atomes du squelette de la CPP extraits du fichier `start.gro`. Généré par `diedre_cpp.py`.

-   **`ramachandran_cpp`**

    -   Image png du diagramme de Ramachandran du peptide CPP. Généré par `ramachandran_cpp.R`.

------------------------------------------------------------------------

## 2. Pré-requis et installation

-   **Python 3.x**
    -   Bibliothèques requises :
        -   `numpy` (pour les calculs vectoriels et numériques)\
        -   `math` (bibliothèque standard Python)\
        -   `csv` (bibliothèque standard Python)\
        -   **BioPython** (si vous utilisez le script `diedre_cpp_biopython.py`)
-   **R**
    -   Version standard pour exécuter `ramachandran_cpp.R`.\
    -   Pas de package R supplémentaire (en dehors de ceux par défaut : `stats`, `utils`, etc.) n’est nécessaire pour la partie graphique.

### Installation

``` bash
# Installer numpy (et BioPython si souhaité) si nécessaire
pip install numpy biopython
```

------------------------------------------------------------------------

## 3. Utilisation

### 3.1 Calcul des angles dièdres avec le script Python custom

``` bash
# Par exemple, pour calculer les angles pour md.gro
python diedre_cpp.py md.gro
```

-   Sortie : un fichier `Angles_md.csv` (le nom varie en fonction du fichier d’entrée).\
-   Le script génère également un fichier texte contenant les coordonnées du squelette, `Coords_squelette_md.txt`.

Pour comparer deux conformations, il est possible de passer plusieurs `.gro` en argument :

``` bash
python diedre_cpp.py md.gro start.gro
```

### 3.2 Calcul avec BioPython

``` bash
python diedre_cpp_biopython.py md.gro
```

-   Sortie : un fichier `Angles_biopython_md.csv`.\
-   Il extrait et calcule les mêmes angles, mais via `Bio.PDB.calc_dihedral`.

De même que pour `diedre_cpp.py`, il est possible de passer plusieurs `.gro` en argument :

``` bash
python diedre_cpp_biopython.py md.gro start.gro
```

### 3.3 Visualisation sous forme de diagramme de Ramachandran (R)

``` bash
Rscript ramachandran_cpp.R
```

-   Le script lit :
    -   `angles_start.csv` et `angles_md.csv`\
    -   `Angles_biopython_start.csv` et `Angles_biopython_md.csv`
-   Il trace et superpose les points (phi, psi) dans un seul diagramme pour les deux méthodes et deux conformations.
-   Le résultat est sauvegardé sous le nom `ramachandran_cpp.png`.

------------------------------------------------------------------------

## 4. Quelques points d’attention

1.  **Conservation du signe**
    -   Dans `calc_prod_scal`, on ne prend pas la valeur absolue pour préserver l’information de signe.\
2.  **Convention de signe du dièdre**
    -   Le script `calc_diedre` utilise un triple produit (produit vectoriel + produit scalaire) pour décider si l’angle est positif ou négatif.\
3.  **Comparaison avec BioPython**
    -   Les angles peuvent différer s’il existe un décalage d’ordre 180° selon la convention ou l’ordre (N, CA, C). Il faut vérifier l’orientation et le nommage des atomes dans le fichier `.gro`.\
4.  **Fichiers `.gro` spécifiques**
    -   Il faut veiller à ce que les atomes N, CA et C soient bien reconnus (l'orthographe doit être la même que dans le script).\
    -   Les scripts ignorent les autres atomes (chaînes latérales, eau, etc.).

------------------------------------------------------------------------

## 5. Auteurs / Contact

-   **Noms** : Laura DUFOUR, Alix FRAGNER\
-   Contact : [laura.dufour\@etu.u-paris.fr](mailto:laura.dufour@etu.u-paris.fr){.email}, [alix.fragner\@etu.u-paris.fr](mailto:alix.fragner@etu.u-paris.fr){.email}
