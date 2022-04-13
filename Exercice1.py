import pandas as pd
#importation du fichier csv pour convertir en dataframe et traiter les données
df_chomage = pd.read_csv("https://www.bfs.admin.ch/bfsstatic/dam/assets/20964153/master", sep = ';')
#verfier s'il y a des données pour toutes les années (2010 à 2020)
print(df_chomage)
for i in range(2010, 2021):
    if any(df_chomage.TIME_PERIOD == i):
        print("Il y a des données pour l'année", i)
    else:
        print("Attention ! Les données de l'année", i, "ne sont pas complètes.")
print("leo")
