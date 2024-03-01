import pandas as pd

data = pd.read_csv('data/all_articles_links.csv', delimiter=',')

# Accéder à la première colonne (supposant que la cellule est dans la première colonne)
cellules = data['Articles url']

# Compter le nombre d'éléments dans chaque cellule
nombre_elements_par_cellule = []
for cellule in cellules:
    elements = cellule.split(',')
    nombre_elements = len(elements)
    nombre_elements_par_cellule.append(nombre_elements)

# Afficher le nombre d'éléments pour chaque ligne
for i, nombre_elements in enumerate(nombre_elements_par_cellule):
    print(f"Ligne {i+1} : Nombre d'éléments : {nombre_elements}")
